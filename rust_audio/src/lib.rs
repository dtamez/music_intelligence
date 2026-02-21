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

#[pyfunction]
fn rms_batch(values: Vec<f32>, frame_size: usize, hop_size: usize) -> Vec<f32> {
    let mut out = Vec::new();
    let mut i = 0;

    while i + frame_size <= values.len() {
        let frame = &values[i..i + frame_size];
        let sum_sq: f32 = frame.iter().map(|v| v * v).sum();
        let rms = (sum_sq / frame.len() as f32).sqrt();
        out.push(rms);
        i += hop_size;
    }

    out
}

#[pymodule]
fn rust_audio(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_values, m)?)?;
    m.add_function(wrap_pyfunction!(rms_energy, m)?)?;
    m.add_function(wrap_pyfunction!(rms_batch, m)?)?;
    Ok(())
}
