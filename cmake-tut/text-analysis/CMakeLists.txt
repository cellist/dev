cmake_minimum_required(VERSION 2.4)
cmake_policy(SET CMP0054 OLD)

# Require dot, treat the other components as optional
find_package(Doxygen
             REQUIRED dot
             OPTIONAL_COMPONENTS mscgen dia)

project(text_analysis)

add_executable(text-analysis text_analysis.cpp word_frequency.cpp)

# Render HTML documentation
set(DOXYGEN_GENERATE_HTML YES)
set(DOXYGEN_GENERATE_MAN NO)

doxygen_add_docs(
  doxygen
  ${PROJECT_SOURCE_DIR}
  COMMENT "Generate HTML pages"
)
