package com.tarea4.notas.DTO;


import java.time.LocalDateTime;

public class AvisoConNotaDTO {
    private Integer id;
    private LocalDateTime fechaPublicacion;
    private String sector;
    private Integer cantidad;
    private String tipo;
    private Integer edad;
    private String comuna;
    private Double notaPromedio;
    private boolean tieneNotas;

    // Constructor
    public AvisoConNotaDTO(Integer id, LocalDateTime fechaPublicacion, String sector, 
                          Integer cantidad, String tipo, Integer edad, String comuna, 
                          Double notaPromedio) {
        this.id = id;
        this.fechaPublicacion = fechaPublicacion;
        this.sector = sector;
        this.cantidad = cantidad;
        this.tipo = tipo;
        this.edad = edad;
        this.comuna = comuna;
        this.notaPromedio = notaPromedio;
        this.tieneNotas = notaPromedio != null;
    }

    // Getters y Setters
    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public LocalDateTime getFechaPublicacion() { return fechaPublicacion; }
    public void setFechaPublicacion(LocalDateTime fechaPublicacion) { this.fechaPublicacion = fechaPublicacion; }

    public String getSector() { return sector; }
    public void setSector(String sector) { this.sector = sector; }

    public Integer getCantidad() { return cantidad; }
    public void setCantidad(Integer cantidad) { this.cantidad = cantidad; }

    public String getTipo() { return tipo; }
    public void setTipo(String tipo) { this.tipo = tipo; }

    public Integer getEdad() { return edad; }
    public void setEdad(Integer edad) { this.edad = edad; }

    public String getComuna() { return comuna; }
    public void setComuna(String comuna) { this.comuna = comuna; }

    public Double getNotaPromedio() { 
        return notaPromedio != null ? Math.round(notaPromedio * 10.0) / 10.0 : null; 
    }
    
    public void setNotaPromedio(Double notaPromedio) { this.notaPromedio = notaPromedio; }

    public boolean isTieneNotas() { return tieneNotas; }
    public void setTieneNotas(boolean tieneNotas) { this.tieneNotas = tieneNotas; }
    
    // Método para obtener la nota como string para la UI
    public String getNotaDisplay() {
        return tieneNotas ? String.valueOf(getNotaPromedio()) : "-";
    }
}