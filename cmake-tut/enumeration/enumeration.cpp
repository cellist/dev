#include <iostream>
#include <string>

class Veggie {
public:
  Veggie(const std::string& name);
  ~Veggie();
  void tellUs();
  
protected:
  std::string myName;
};

Veggie::Veggie(const std::string& name) {
  myName = name;
}

Veggie::~Veggie() {
  std::cout << myName << " - good bye!" << std::endl;
}

void Veggie::tellUs() {
  std::cout << "I am a(n) '" << myName << "'." << std::endl;
}

typedef enum veggies {
		      VEGGIE_FIRST = 0,
		      APPLE,
		      BANANA,
		      CHERRY,
		      DATE,
		      EGGPLANT,
		      FIG,
		      GRAPE,
		      VEGGIE_LAST
} veggies_t;

typedef struct veggie_table_entry {
  veggies_t   kind;
  Veggie*     aVeggie;
} veggie_table_entry_t;

int main() {
  veggie_table_entry_t veggies[] = {
				    { APPLE,        new Veggie("APPLE") },
				    { BANANA,       new Veggie("BANANA") },
				    { CHERRY,       new Veggie("CHERRY") },
				    { DATE,         new Veggie("DATE") },
				    { EGGPLANT,     new Veggie("EGGPLANT") },
				    { FIG,          new Veggie("FIG") },
				    { GRAPE,        new Veggie("GRAPE") }
  };

  const int vmax =  sizeof(veggies) / sizeof(veggie_table_entry_t);
  
  for(int v = 0; v < vmax; v++) {
    std::cout << veggies[v].kind << ": ";
    veggies[v].aVeggie->tellUs();
    delete veggies[v].aVeggie;
  }
  return 0;
}
