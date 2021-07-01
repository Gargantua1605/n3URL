# n3URL : Controlling game movement with EEG data using CNNs

### Goal

To collect information about a person's thoughts using an EEG and enabling them to control movement in the classic Atari game breakout just by thinking, all without needing to press a single button!

An EEG (Electro-Encephalo-Gram) consists of several tiny electrodes placed on the skull to record electrical activity on the scalp. These signals are generated because of signalling between the underlying neurons of the brain.

### Repository Structure

+ We recreated the classic game Breakout using the *PyGame* library. The game consists of a moving paddle that reflects a bouncing ball. Whenever the wall touches bricks it destroys them and rebounds. The objective of the game is to destroy as many bricks as possible without letting the ball fall on the ground. There are only two types of paddle movement, left and right.

+ We trained a Convolutional neural Network (CNN) using the motor movement/imagery data for left and right directions. The network was developed using *TensorFlow Keras*. After exploring a variety of network architectures and data inputs we have chosen the following architecture which gives us ( ) accuracy.

  Architecture:
  - Layers
    ( )
  - Input Data
    ( )
  - Confusion Matrix
    ( )

  We are still exploring alternative architectures and will continue to update this repository as accuracy improves.

+ Interfacing with the headset

  (to be added)

+ Real-time classification using the CNN    

  (to be added)


### References

This project uses the EEG Motor Movement/Imagery Dataset

[Schalk, G., McFarland, D.J., Hinterberger, T., Birbaumer, N., Wolpaw, J.R. BCI2000: A General-Purpose Brain-Computer Interface (BCI) System. IEEE Transactions on Biomedical Engineering 51(6):1034-1043, 2004.](http://www.ncbi.nlm.nih.gov/pubmed/15188875)

Goldberger, A., L. Amaral, L. Glass, J. Hausdorff, P. C. Ivanov, R. Mark, J. E. Mietus, G. B. Moody, C. K. Peng, and H. E. Stanley. "PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. Circulation [Online]. 101 (23), pp. e215–e220." (2000).
