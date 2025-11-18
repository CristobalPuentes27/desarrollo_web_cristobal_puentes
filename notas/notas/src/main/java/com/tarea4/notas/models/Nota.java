package com.tarea4.notas.models;

import jakarta.persistence.*;


@Entity
@Table(name = "nota")
public class Nota {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "aviso_id", nullable = false)
    private AvisoAdopcion aviso;
    
    @Column(name = "nota", nullable = false)
    private Integer nota;
    
    // CONSTRUCTORES
    public Nota() {}
    
    public Nota(AvisoAdopcion aviso, Integer nota) {
        this.aviso = aviso;
        this.nota = nota;
    }
    
    // GETTERS Y SETTERS
    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    
    public AvisoAdopcion getAviso() { return aviso; }
    public void setAviso(AvisoAdopcion aviso) { this.aviso = aviso; }
    
    public Integer getNota() { return nota; }
    public void setNota(Integer nota) { this.nota = nota; }
}