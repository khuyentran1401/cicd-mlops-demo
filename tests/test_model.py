from deepchecks.tabular.checks import (ModelInferenceTime, PredictionDrift,
                                       SimpleModelComparison,
                                       TrainTestPerformance)


def test_model_inference_time(model, test_data):
    """Check measures the model's average inference time per sample. Fast runtime
    can significantly impact the user experience or the system load."""
    check = ModelInferenceTime()
    result = check.run(test_data, model)
    assert result.passed_conditions()


def test_prediction_drift(train_data, test_data, model):
    """Detect if there is a drift in the predictions. A drift indicates that a changed
    has happened in the data that actually affects model predictions."""
    check = PredictionDrift()
    result = check.run(train_data, test_data, model)
    assert result.passed_conditions()


def test_simple_model_comparison(model, train_data, test_data):
    """The simple model is used as a baseline for the minimum model performance.
    If a user's model fails to surpass the simple model's performance, it may
    imply potential issues with the model.
    """
    check = SimpleModelComparison()
    result = check.run(train_data, test_data, model)
    assert result.passed_conditions()


def test_train_test_performance(model, train_data, test_data):
    """Compare model’s performance between the train and test datasets based on multiple scorers."""
    check = TrainTestPerformance(
        scorers=["neg_mean_absolute_error", "neg_mean_squared_error", "r2"]
    )
    result = check.run(train_data, test_data, model)
    assert result.passed_conditions()
