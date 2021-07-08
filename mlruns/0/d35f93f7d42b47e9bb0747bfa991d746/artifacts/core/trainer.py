from mlflow import log_metric, log_artifacts

class Trainer:
    def __init__(self, model, loss_fn, optim):
        self.model = model
        self.loss_fn = loss_fn
        self.optim = optim

    def train(self, epochs, x_train, y_train):
        self.model.train()

        for t in range(epochs):
            self.optim.zero_grad()

            output = self.model(x_train)
            
            loss = self.loss_fn(output, y_train)
            if t % 10 == 0 and t !=0:
                log_metric('Loss', loss.item())
                print("Epoch ", t, "MSE: ", loss.item())

            loss.backward()

            self.optim.step()

        log_artifacts("src")
        
        return output

    def test(self):
        raise NotImplementedError()
