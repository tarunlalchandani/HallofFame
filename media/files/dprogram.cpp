#include<iostream> 
using namespace std;
int main(){
	float overall = 0;
	float m = 0,pm= 0 ;
	float a = 0,pa= 0;
	float q= 0 ,pq = 0;
	float f = 0,pf = 0;
	cout<<"Enter the midterm mark and its percentage: ";
	cin>>m>>pm;
	cout<<"Enter the assignments mark and its percentage: ";
	cin>>a>>pa;
	cout<<"Enter the quizzes mark and its percentage: ";
	cin>>q>>pq;
	cout<<"Enter the final mark and its percentage: ";
	cin>>f>>pf;
	overall = 100;
	float  total = (m*pm+a*pa+q*pq+f*pf);
	float ans = (total*100)/overall;
	cout<<"The overall mark is "<<ans/100;
	return 0;	
	
}
