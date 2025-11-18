package com.tarea4.notas.DTO;

public class EvaluacionRequestDTO {
    private Integer avisoId;
    private Integer nota;

    // Constructor vacío necesario para Jackson
    public EvaluacionRequestDTO() {}

    // Constructor
    public EvaluacionRequestDTO(Integer avisoId, Integer nota) {
        this.avisoId = avisoId;
        this.nota = nota;
    }

    // Getters y Setters
    public Integer getAvisoId() { return avisoId; }
    public void setAvisoId(Integer avisoId) { this.avisoId = avisoId; }

    public Integer getNota() { return nota; }
    public void setNota(Integer nota) { this.nota = nota; }
}