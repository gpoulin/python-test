void rescale(double* data, double* out, int l, double offset, double scale){
  int i=0;
  for (i=0; i<l; ++i){
    out[i]=(data[i]-offset)*scale;
  }
}
