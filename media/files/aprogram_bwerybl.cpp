#include<iostream>
using namespace std;
int main(){
	char ch;
	int n;
	cout<<"Enter the code and the number of gallons: ";
	cin>>ch>>n;
	float cost = 0;
	if(ch=='h'){
		cost = 5;
		cost += n*0.05;
	}
	else if(ch=='c'){
		if(n<=4000){
			cost = 100.00;
		}
		else{
			cost  =100.00;
			int extra = n-4000;
			cost += extra*0.025;
		}
	}
	else if(ch=='i'){
		if(n<=4000){
			cost = 1500;
		}
		else if(n>4000 and n<=10000){
			cost = 2500;
		}		
		else{
			cost = 3500;
		}
	}
	cout<<"The water bill is "<<cost<<" dirham";
}
