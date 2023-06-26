#include <iostream>
#include <cstring>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <thread>

void sendRequest(int clientSocket) {
    const char* request = "Hello from client!";
    send(clientSocket, request, strlen(request), 0);

    char buffer[1024];
    memset(buffer, 0, sizeof(buffer));

    // Receive response from the server
    int bytesRead = recv(clientSocket, buffer, sizeof(buffer) - 1, 0);
    if (bytesRead <= 0) {
        std::cerr << "Error reading from server" << std::endl;
        return;
    }

    std::cout << "Received from server: " << buffer << std::endl;

    // Close the client socket
    close(clientSocket);
}

int main() {
    const int numThreads = 5;
    const std::string serverAddress = "127.0.0.1"; // Change server IP address if necessary
    const int serverPort = 1234; // Change server port number if necessary

    for (int i = 0; i < numThreads; i++) {
        // Create a socket
        int clientSocket = socket(AF_INET, SOCK_STREAM, 0);
        if (clientSocket < 0) {
            std::cerr << "Failed to create socket" << std::endl;
            return 1;
        }

        struct sockaddr_in serverAddressInfo;
        serverAddressInfo.sin_family = AF_INET;
        serverAddressInfo.sin_port = htons(serverPort);
        if (inet_pton(AF_INET, serverAddress.c_str(), &(serverAddressInfo.sin_addr)) <= 0) {
            std::cerr << "Invalid server address" << std::endl;
            return 1;
        }

        // Connect to the server
        if (connect(clientSocket, (struct sockaddr*)&serverAddressInfo, sizeof(serverAddressInfo)) < 0) {
            std::cerr << "Failed to connect to server" << std::endl;
            return 1;
        }

        // Send request and receive response in a separate thread
        std::thread requestThread(sendRequest, clientSocket);
        requestThread.detach();
    }

    // Sleep for a while to allow the threads to complete
    std::this_thread::sleep_for(std::chrono::seconds(5));

    return 0;
}
