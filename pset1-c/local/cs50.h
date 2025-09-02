#pragma once
#include <stdbool.h>

typedef const char* string;

int get_int(const char *prompt);
long get_long(const char *prompt);
float get_float(const char *prompt);
double get_double(const char *prompt);
bool get_bool(const char *prompt);
