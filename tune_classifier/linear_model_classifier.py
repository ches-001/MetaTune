import random
from baseline import SampleClassMixin
from optuna.trial import Trial
from dataclasses import dataclass
from typing import Iterable, Optional, Dict, Any
from sklearn.linear_model import LogisticRegression
from utils.linear_model_utils import get_valid_solver_info

@dataclass
class LogisticRegressionModel(SampleClassMixin):
    penalty_space: Iterable[bool] = ("l1", "l2", "elasticnet", None)
    dual_space: Iterable[bool] = (True, False)
    tol_space: Iterable[float] = (1e-6, 1e-3)
    C_space: Iterable[float] = (0.9, 1.0)
    fit_intercept_space: Iterable[bool] = (True, False)
    intercept_scaling_space: Iterable[float] = (0.5, 1.0)
    class_weight_space: Iterable[str] = ("balanced", )
    solver_space: Iterable[str] = ("lbfgs", "liblinear", "newton-cg", "newton-cholesky", "sag", "saga")
    max_iter_space: Iterable[int] = (100, 1000)
    multi_class_space: Iterable[str] = ("auto", )
    l1_ratio_space: Iterable[float] = (0.0, 1.0)
    model: Any = None
    
    def _sample_params(self, trial: Optional[Trial]=None) -> Dict[str, Any]:
        super()._sample_params(trial)
        
        params = {}
        params["penalty"] = trial.suggest_categorical("penalty", self.penalty_space)
        params["dual"] = trial.suggest_categorical("dual", self.dual_space)
        params["tol"] = trial.suggest_float("tol", *self.tol_space, log=False)
        params["C"] = trial.suggest_float("C", *self.C_space, log=False)
        params["fit_intercept"] = trial.suggest_categorical("fit_intercept", self.fit_intercept_space)
        params["intercept_scaling"] = trial.suggest_float("intercept_scaling", *self.intercept_scaling_space, log=False)
        params["class_weight"] = trial.suggest_categorical("class_weight", self.class_weight_space)
        params["solver"] = trial.suggest_categorical("solver", self.solver_space)
        params["max_iter"] = trial.suggest_int("max_iter", *self.max_iter_space, log=False)
        params["multi_class"] = trial.suggest_categorical("multi_class", self.multi_class_space)
        params["l1_ratio"] = trial.suggest_float("l1_ratio", *self.l1_ratio_space, log=False)

        valid_solver_info: Iterable = get_valid_solver_info(params["solver"])

        params["dual"] = valid_solver_info["dual"]
        trial.set_user_attr("dual", params["dual"])

        if params["penalty"] not in valid_solver_info["penalties"]:
            params["penalty"] = random.choice(valid_solver_info["penalties"])
            trial.set_user_attr("penalty", params["penalty"])

        if params["penalty"] != "elasticnet":
            params["l1_ratio"] = None
            trial.set_user_attr("l1_ratio", params["l1_ratio"])

        if params["penalty"] is None:
            params["C"] = 1.0
            trial.set_user_attr("C", params["C"])

        if params["penalty"] == "l1":
            params["dual"] = False
            trial.set_user_attr("dual", params["dual"])
 
        return params
    
    def sample_model(self, trial: Optional[Trial]=None) -> Any:
        super().model(trial)
        
        params = self._sample_params(trial)
        model = LogisticRegression(**params)
        
        self.model = model
        return model