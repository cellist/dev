#include <iostream>
#include <iomanip>
#include <string>

/*
** You can ask the preprocessor directly like so:
** - echo | clang++ -x c++ -std=c++11 -dM -E - | sort -u
** - echo | g++ -x c++ -std=c++11 -dM -E - | sort -u
*/
typedef struct define_status {
    std::string name;
    bool        defined;
} define_status_t;

int main() {

  const define_status_t checklist[] = {
		   { "__clang__",
		     #ifdef __clang__
		     true
		     #else
		     false
		     #endif
		   },
		   { "__cplusplus",
		     #ifdef __cplusplus
		     true
		     #else
		     false
		     #endif
		   },
		   { "__gnu_linux__",
		     #ifdef __gnu_linux__
		     true
		     #else
		     false
		     #endif
		   },
		   { "__linux",
		     #ifdef __linux
		     true
		     #else
		     false
		     #endif
		   },
		   { "__linux__",
		     #ifdef __linux__
		     true
		     #else
		     false
		     #endif
		   },
		   { "__llvm__",
		     #ifdef __llvm__
		     true
		     #else
		     false
		     #endif
		   },
		   { "__GNUC__",
		     #ifdef __GNUC__
		     true
		     #else
		     false
		     #endif
		   },
		   { "__STDC__",
		     #ifdef __STDC__
		     true
		     #else
		     false
		     #endif
		   },
		   { "__STDC_VERSION__",
		     #ifdef __STDC_VERSION__
		     true
		     #else
		     false
		     #endif
		   },
		   { "__USE_GNU",
		     #ifdef __USE_GNU
		     true
		     #else
		     false
		     #endif
		   },
		   { "__USE_ISOC11",
		     #ifdef __USE_ISOC11
		     true
		     #else
		     false
		     #endif
		   },
		   { "__USE_ISOC99",
		     #ifdef __USE_ISOC99
		     true
		     #else
		     false
		     #endif
		   },
		   { "__USE_POSIX",
		     #ifdef __USE_POSIX
		     true
		     #else
		     false
		     #endif
		   },
		   { "__USE_POSIX2",
		     #ifdef __USE_POSIX2
		     true
		     #else
		     false
		     #endif
		   },
		   { "__USE_POSIX199309",
		     #ifdef __USE_POSIX199309
		     true
		     #else
		     false
		     #endif
		   },
		   { "__USE_POSIX199506",
		     #ifdef __USE_POSIX199506
		     true
		     #else
		     false
		     #endif
		   },
		   { "__USE_UNIX98",
		     #ifdef __USE_UNIX98
		     true
		     #else
		     false
		     #endif
		   },
		   { "__USE_XOPEN_EXTENDED",
		     #ifdef __USE_XOPEN_EXTENDED
		     true
		     #else
		     false
		     #endif
		   },
		   { "__USE_XOPEN2K",
		     #ifdef __USE_XOPEN2K
		     true
		     #else
		     false
		     #endif
		   },
		   { "__USE_XOPEN2K8",
		     #ifdef __USE_XOPEN2K8
		     true
		     #else
		     false
		     #endif
		   },
		   { "__USE_XOPEN2KXSI",
		     #ifdef __USE_XOPEN2KXSI
		     true
		     #else
		     false
		     #endif
		   },
		   { "_GNU_SOURCE",
		     #ifdef _GNU_SOURCE
		     true
		     #else
		     false
		     #endif
		   },
		   { "_LIBC",
		     #ifdef _LIBC
		     true
		     #else
		     false
		     #endif
		   },
		   { "_XOPEN_SOURCE",
		     #ifdef _XOPEN_SOURCE
		     true
		     #else
		     false
		     #endif
		   },
		   { "_XOPEN_SOURCE_EXTENDED",
		     #ifdef _XOPEN_SOURCE_EXTENDED
		     true
		     #else
		     false
		     #endif
		   },
		   { "HAVE_TYPE_TRAITS",
		     #ifdef HAVE_TYPE_TRAITS
		     true
		     #else
		     false
		     #endif
		   },
		   { "linux",
		     #ifdef linux
		     true
		     #else
		     false
		     #endif
		   },
		   { "STDC",
		     #ifdef STDC
		     true
		     #else
		     false
		     #endif
		   },
		   { "SYS16BIT",
		     #ifdef SYS16BIT
		     true
		     #else
		     false
		     #endif
		   },
		   { "unix",
		     #ifdef unix
		     true
		     #else
		     false
		     #endif
		   },
		   { "VMS",
		     #ifdef VMS
		     true
		     #else
		     false
		     #endif
		   },
		   { "WIN32",
		     #ifdef WIN32
		     true
		     #else
		     false
		     #endif
		   }
  };

  std::cout << "CHECKING FOR SOME DEFINES:" << std::endl;
  for(int i = 0; i < sizeof(checklist) / sizeof(define_status_t); i++) {
    std::cout << std::setw(3) << std::right << i << ": "
	      << std::setw(23) << std::left << checklist[i].name
	      << (checklist[i].defined ? " is" : " is _NOT_")
	      << " defined." << std::endl;
  }
  return 0;
}
