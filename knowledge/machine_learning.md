# Machine Learning

## Linear Regression
Linear regression predicts a continuous target using a linear relationship between input features and the target.

For one feature, a simple model can be written as:

y_pred = w*x + b

where w is the weight and b is the bias.

## Gradient Descent
Gradient descent is an optimization algorithm used to minimize a loss function.

The general update rule is:

parameter_new = parameter_old - learning_rate * gradient

The gradient indicates the direction in which the loss increases. Therefore, subtracting the gradient moves the parameter toward lower loss.

## Logistic Regression
Logistic regression is commonly used for binary classification. It computes a linear combination of the input features and passes the result through the sigmoid function.

sigmoid(z) = 1 / (1 + exp(-z))

The output is between 0 and 1 and can be interpreted as a probability for the positive class.

## Overfitting
Overfitting occurs when a model learns the training data too closely, including noise or accidental patterns. Such a model can perform well on training data but poorly on unseen data.

Common ways to reduce overfitting include regularization, collecting more data, simplifying the model, data augmentation, and early stopping.
