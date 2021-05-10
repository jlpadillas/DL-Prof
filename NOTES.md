# Notes

In the neural network terminology:

- one __epoch__ = one forward pass and one backward pass of _all_ the training examples

- __batch size__ = the number of training examples in one forward/backward pass. The higher the batch size, the more memory space you'll need.

- number of __iterations__ = number of passes, each pass using [batch size] number of examples. To be clear, one pass = one forward pass + one backward pass (we do not count the forward pass and backward pass as two different passes).

Example: if you have 1000 training examples, and your batch size is 500, then it will take 2 iterations to complete 1 epoch.
