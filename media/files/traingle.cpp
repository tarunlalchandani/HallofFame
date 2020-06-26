#include<iostream>
using namespace std;
int main(){
	int a,b;
	cout<<"Enter the two angles in degrees: ";
	cin>>a>>b;
	int c = 180-a-b;
	cout<<"The third angle is "<<c;
	if(a==b and b==c){
		cout<<endl<<"The traingle is equilateral";
	}
	else if(a==b or b==c or c==a){
		cout<<endl<<"The traingle is isosceles";
	}
	return 0;
}
