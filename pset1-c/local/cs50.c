#include "cs50.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void promptf(const char *prompt)
{
    if (prompt && *prompt)
    {
        fputs(prompt, stdout);
        fflush(stdout);
    }
}

int get_int(const char *prompt)
{
    int v; char c;
    while (1)
    {
        promptf(prompt);
        if (scanf(" %d%c", &v, &c) == 2 && (c=='\n' || c==' '))
            return v;
        // clear line
        int ch; while ((ch = getchar()) != '\n' && ch != EOF) {}
        fputs("Retry: ", stdout);
    }
}

long get_long(const char *prompt)
{
    long v; char c;
    while (1)
    {
        promptf(prompt);
        if (scanf(" %ld%c", &v, &c) == 2 && (c=='\n' || c==' '))
            return v;
        int ch; while ((ch = getchar()) != '\n' && ch != EOF) {}
        fputs("Retry: ", stdout);
    }
}

float get_float(const char *prompt)
{
    float v; char c;
    while (1)
    {
        promptf(prompt);
        if (scanf(" %f%c", &v, &c) == 2 && (c=='\n' || c==' '))
            return v;
        int ch; while ((ch = getchar()) != '\n' && ch != EOF) {}
        fputs("Retry: ", stdout);
    }
}

double get_double(const char *prompt)
{
    double v; char c;
    while (1)
    {
        promptf(prompt);
        if (scanf(" %lf%c", &v, &c) == 2 && (c=='\n' || c==' '))
            return v;
        int ch; while ((ch = getchar()) != '\n' && ch != EOF) {}
        fputs("Retry: ", stdout);
    }
}

bool get_bool(const char *prompt)
{
    char buf[8];
    while (1)
    {
        promptf(prompt);
        if (scanf(" %7s", buf) == 1)
        {
            if (buf[0]=='y'||buf[0]=='Y'||buf[0]=='1'||buf[0]=='t'||buf[0]=='T') return true;
            if (buf[0]=='n'||buf[0]=='N'||buf[0]=='0'||buf[0]=='f'||buf[0]=='F') return false;
        }
        int ch; while ((ch = getchar()) != '\n' && ch != EOF) {}
        fputs("Retry: ", stdout);
    }
}

string get_string(const char *prompt)
{
    promptf(prompt);
    size_t cap = 64;
    char *buf = (char*)malloc(cap);
    if (!buf) exit(1);
    size_t len = 0;
    int ch;
    while ((ch = getchar()) != '\n' && ch != EOF)
    {
        if (len + 1 >= cap)
        {
            cap *= 2;
            char *tmp = (char*)realloc(buf, cap);
            if (!tmp) { free(buf); exit(1); }
            buf = tmp;
        }
        buf[len++] = (char)ch;
    }
    buf[len] = '\0';
    return buf;
}
