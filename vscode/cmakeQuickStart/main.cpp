#include <map>
#include <vector>
#include <string>
#include <iostream>
#include <iomanip>

typedef std::vector<std::string> words_t;
typedef std::map<std::size_t, words_t> wordmap_t;

void insertWord(wordmap_t &wmap, std::string &value)
{
    std::size_t len = value.size();

    if (wmap.count(len))
    {
        wmap.at(len).push_back(value);
    }
    else
    {
        words_t w;
        w.push_back(value);
        wmap[len] = w;
    }
}

int main(int argc, char *argv[])
{
    wordmap_t wmap;
    words_t words = {
        "Franz",
        "jagt",
        "im",
        "komplett",
        "verwahrlosten",
        "Taxi",
        "quer",
        "durch",
        "Bayern"};

    for (words_t::iterator it = words.begin(); it != words.end(); it++)
    {
        insertWord(wmap, *it);
    }

    for (wordmap_t::iterator it = wmap.begin(); it != wmap.end(); it++)
    {
        std::cout << std::setw(2) << it->first << ":";
        for (int i = 0; i < it->second.size(); i++)
        {
            std::cout << " [" << it->second.at(i) << "]";
        }
        std::cout << std::endl;
    }
}
