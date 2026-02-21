use pyo3::prelude::*;

#[pyfunction]
fn sum_values(values: Vec<f32>) -> f32 {
    values.iter().sum()
}

// measure the average energy of all the samples
#[pyfunction]
fn rms_energy(values: Vec<f32>) -> f32 {
    let sum_sq: f32 = values.iter().map(|v| v * v).sum();
    (sum_sq / values.len() as f32).sqrt()
}

#[pymodule]
fn rust_audio(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_values, m)?)?;
    m.add_function(wrap_pyfunction!(rms_energy, m)?)?;
    Ok(())
}
