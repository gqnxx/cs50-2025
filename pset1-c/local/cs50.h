#pragma once
#include <stdbool.h>

typedef char* string;

int get_int(const char *prompt);
long get_long(const char *prompt);
float get_float(const char *prompt);
double get_double(const char *prompt);
bool get_bool(const char *prompt);
string get_string(const char *prompt);
