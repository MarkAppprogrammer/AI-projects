## Cool Ai Projects

# Voice Project

Attempting to make bc-resnet model. Faced unequal stried problem in tensorflow so switching to pytorch. code is written 95% manually by me which is why it is also not the most efficent method.

### References
- [1st Paper](#)
- [2nd Paper](#)
- [Google Database](#)

### Model Scaling
To scale the BC-ResNet model, increase the channel width by a factor of `x` to derive BC-ResNet-x from BC-ResNet-1. BC-ResNet-3 is recommended for the best balance between accuracy and parameter efficiency.

### Key Equation
The model follows the equation:  
`y = x + f_2(x) + BC(f_1(avgpool(f_2(x))))`

### Input Features
- Input feature `x` dimensions: `h x w`  
    - `h`: Frequency  
    - `w`: Time  

### Components
1. **F_2**:  
     - 3x1 frequency depthwise convolution  
     - SSN with subbands=5  
     - Averaging reduces dimensions to `1 x w`  

2. **F_1**:  
     - 1x3 temporal depthwise convolution  
     - Batch Normalization (BN)  
     - Swish activation  
     - 1x1 pointwise convolution  
     - Dropout (rate `p=0.1`)  

3. **Broadcast Operation**:  
     - Expands dimensions from `1 x w` to `h x w`  

4. **Auxiliary 2D Residual Connection**:  
     - Adds `x` and `f_2(x)` to the broadcasted output  

### Notes
- Avoid using stride and dilation simultaneously.  
    - Use stride for frequency depthwise convolution (f-dw).  
    - Use dilation for temporal depthwise convolution (t-dw).  

### Translation Block
- Handles differing input and output channels.  
- No residual connection from `input_tensor`.  
- Begins with a `1x1` convolution, followed by BN and ReLU in `f_2`.

### Implementation Details
- **Data Augmentation**:  
    - Random time shift: `-100ms` to `100ms`  
    - Background noise: Probability `0.8`  
        - Noise added from Google Speech Commands databases (v1 and v2)  

- **Audio Input Features**:  
    - 40-dimensional log mel spectrograms  
    - 30ms window size with 10ms frame shift  

- **SpecAugment**:  
    - Applied for further augmentation.