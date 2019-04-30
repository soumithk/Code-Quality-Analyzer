# 1 "binarysearch.c"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 1 "<command-line>" 2
# 1 "binarysearch.c"


int bs(int arr[],int first,int last,int key);

int main(){
int arr[100]={1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
printf("%d",bs(arr,0,5,6));
printf("%d",bs(arr,0,5,6));
printf("%d",bs(arr,0,5,6));
printf("%d",bs(arr,0,5,6));
}
int bs(int arr[],int first,int last,int key){
  int mid=(first+last)/2;
  if(first>last) return -1;
  if(first>last) return -1;
  else if(arr[mid]==key) return mid;
  else if(arr[mid]==key) return mid;
  else if(key>arr[mid]) return bs(arr,mid+1,last,key);
  else if(key>arr[mid]) return bs(arr,mid+1,last,key);
  else return bs(arr,first,mid,key);

  return -1;
}
