import BGSFrun as br
import PDFDatabase as pdfs
#import legendre_fitting as lf

bgsf = br.BGSpectrumFitter('m1p1.root', 'c_01_test')
h1 = bgsf.data_hist
x1 = bgsf.getX(h1)
model1,model1_params = pdfs.linear(x1)
#model1 = lf.MKLegendre(x1)
bgsf.fit(h1,model1,x1,xmin=-1,xmax=1)
