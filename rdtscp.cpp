//make global
bool reset = true;
unsigned int recordingCount = 0;
const unsigned int dumpCount = 1000;
unsigned __int64 start, stop, totalTime;
unsigned int aux1, aux2;
unsigned __int64 min, max;

#define azlStartTimer                       \
{                                           \
    if (reset)                              \
    {                                       \
        reset = false;                      \
        recordingCount = 0;                 \
        totalTime = 0;                      \
        min = ((unsigned __int64)0) - 1;    \
        max = 0;                            \
    }                                       \
    start = __rdtscp(&aux1);                \
}

//time here

#define azlStopTimer                        \
{                                           \
    stop = __rdtscp(&aux2);                 \
    if (aux1 == aux2)                       \
    {                                       \
        totalTime += stop - start;          \
        if ((stop - start) > max)           \
            max = stop - start;             \
        if ((stop - start) < min)           \
            min = stop - start;             \
        recordingCount++;                   \
        if (recordingCount >= dumpCount)    \
        {                                   \
            totalTime /= dumpCount;         \
            char prettyPrint[100];          \
            sprintf(prettyPrint, "cycles: %llu \tmin: %llu\tmax: %llu\n", totalTime, min, max); \
            OutputDebugString(prettyPrint); \
            reset = true;                   \
        }                                   \
    }                                       \
}