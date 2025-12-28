package com.tarea4.notas.DTO;


public class EvaluacionResponseDTO {
    private boolean success;
    private String message;
    private Double nuevoPromedio;

    // Constructores
    public EvaluacionResponseDTO() {}

    public EvaluacionResponseDTO(boolean success, String message, Double nuevoPromedio) {
        this.success = success;
        this.message = message;
        this.nuevoPromedio = nuevoPromedio;
    }

    // Getters y Setters
    public boolean isSuccess() { return success; }
    public void setSuccess(boolean success) { this.success = success; }

    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }

    public Double getNuevoPromedio() { return nuevoPromedio; }
    public void setNuevoPromedio(Double nuevoPromedio) { this.nuevoPromedio = nuevoPromedio; }
}