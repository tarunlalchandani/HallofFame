#include<iostream>
using namespace std;
int main(){
	int n;
	cout<<"Enter a number: ";
	cin>>n1;
	int n = n1
	int arr[6];
	int i = 0;
	while(n!=0){
		int temp = n%10;
		n = n/10;
		arr[i++] = temp;
	}
	int day = arr[1]*10+arr[0];
	int month = arr[3]*10 + arr[2];
	int year = arr[5]*10+arr[4];
	year = 2000+year;
	cout<<"The number "<<n<<" represents the date "<<month<<"/"<<day<<"/"<<year;
	return 0;
}
