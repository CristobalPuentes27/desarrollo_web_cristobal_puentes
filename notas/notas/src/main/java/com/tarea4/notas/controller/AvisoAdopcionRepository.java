package com.tarea4.notas.controller;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.util.List;
import com.tarea4.notas.models.AvisoAdopcion;

@Repository
public interface AvisoAdopcionRepository extends JpaRepository<AvisoAdopcion, Integer> {
    
    // Encontrar todos los avisos con join a comuna
    @Query("SELECT a FROM AvisoAdopcion a JOIN FETCH a.comuna c JOIN FETCH c.region ORDER BY a.fechaIngreso DESC")
    List<AvisoAdopcion> findAllWithComunaAndRegion();
}