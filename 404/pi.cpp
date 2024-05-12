#include <iostream>
#include <random>
#include <numeric>
#include <cmath>

// Function to estimate pi using the probability two numbers are relatively prime
double estimatePi(int numPairs) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(1, 100000);

    int numRelativelyPrime = 0;
    for (int i = 0; i < numPairs; ++i) {
        int a = dis(gen);
        int b = dis(gen);
        if (std::gcd(a, b) == 1) {
            numRelativelyPrime++;
        }
    }
    double probability = static_cast<double>(numRelativelyPrime) / numPairs;
    return std::sqrt(6 / probability);
}

int main() {
    int numPairs = 1000000; // Number of pairs to generate
    double piEstimate = estimatePi(numPairs);
    std::cout << "Estimated value of Pi: " << piEstimate << std::endl;

    return 0;
}
