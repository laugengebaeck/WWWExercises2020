#include<bits/stdc++.h>

using namespace std;

int main(){
    std::ostringstream std_input; 
    std_input << std::cin.rdbuf(); 
    std::string text = std_input.str();

    map<char,int> occ;
    
    for(auto c : text){
        if(occ.count(c) == 0){
            occ[c] = 1;
        } else {
            occ[c]++;
        }
    }

    double sum = 0;
    int n = text.length(), sum2 = 0;
    for(auto p : occ){
        cout << ((p.first != '\n') ? p.first : '@') << " " << p.second << "\n";
        sum2 += p.second;
        double pj = p.second;
        sum += -(pj/n) * log2(pj/n);
        //cout << "+ -(" << p.second << "/" << n << ") * (" << log2(pj/n) << ") ";
    }
    //cout << "\n = " << sum << "\n";

    cout << sum2 << "\n";

    return 0;
}