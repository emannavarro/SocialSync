import sys
from PyQt5.QtWidgets import QApplication
from ui.pyqt.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


'''

urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
Base Path: /var/folders/0d/jj7yr0n95z5gj06tmsc9y3_80000gn/T/_MEIZOTi5g
Parent Directory: /var/folders/0d/jj7yr0n95z5gj06tmsc9y3_80000gn/T
Haar Cascade Path: /var/folders/0d/jj7yr0n95z5gj06tmsc9y3_80000gn/T/ml/haarcascade_frontalface_default.xml
Model Path: /var/folders/0d/jj7yr0n95z5gj06tmsc9y3_80000gn/T/ml/model.h5
[ERROR:0@25.183] global persistence.cpp:512 open Can't open file: '/var/folders/0d/jj7yr0n95z5gj06tmsc9y3_80000gn/T/ml/haarcascade_frontalface_default.xml' in read mode
Error loading Haar Cascade: Failed to load Haar Cascade from       /var/folders/0d/jj7yr0n95z5gj06tmsc9y3_80000gn/T/ml/haarcascade_frontalface_default.xml
                                                                   /var/folders/0d/jj7yr0n95z5gj06tmsc9y3_80000gn/T/ml/haarcascade_frontalface_default.xmlop
                                                                   
                                                                   
                                                                   
  
 urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
Base Path: /var/folders/0d/jj7yr0n95z5gj06tmsc9y3_80000gn/T/_MEIaejwPY
Parent Directory: /var/folders/0d/jj7yr0n95z5gj06tmsc9y3_80000gn/T
Haar Cascade Path:                                                 /var/folders/0d/jj7yr0n95z5gj06tmsc9y3_80000gn/T/ml/haarcascade_frontalface_default.xm
Model Path: /var/folders/0d/jj7yr0n95z5gj06tmsc9y3_80000gn/T/ml/model.h5
[ERROR:0@28.209] global persistence.cpp:512 open Can't open file: '/var/folders/0d/jj7yr0n95z5gj06tmsc9y3_80000gn/T/ml/haarcascade_frontalface_default.xm' in read mode
Error loading Haar Cascade: Failed to load Haar Cascade from       /var/folders/0d/jj7yr0n95z5gj06tmsc9y3_80000gn/T/ml/haarcascade_frontalface_default.xm

                                                                  
                                                                   
                                                                   
                                                                   
'''