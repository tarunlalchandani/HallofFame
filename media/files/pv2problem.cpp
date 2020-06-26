#include<iostream>
using namespace std;
int main(){
	int l = 0, u =0 ;
	int k = 0;
	cout<<"Enter the lower and upper limits of an interval: ";
	cin>>l>>u;
	cout<<"Enter a number within the interval["<<l<<" "<<u<<"]: ";
	cin>>k;
	int pos = k-l+1;
	cout<<"The number "<<k<<" is the "<<pos<<"th number";
	return 0;
}
