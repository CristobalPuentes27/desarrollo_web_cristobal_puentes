package com.tarea4.notas.controller;


import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;
import com.tarea4.notas.models.Nota;

@Repository
public interface NotaRepository extends JpaRepository<Nota, Integer> {
    
    // Encontrar todas las notas de un aviso
    List<Nota> findByAvisoId(Integer avisoId);
    
    // Calcular promedio de notas de un aviso
    @Query("SELECT AVG(n.nota) FROM Nota n WHERE n.aviso.id = :avisoId")
    Double findPromedioByAvisoId(@Param("avisoId") Integer avisoId);
    
    // Contar cantidad de notas por aviso
    @Query("SELECT COUNT(n) FROM Nota n WHERE n.aviso.id = :avisoId")
    Long countByAvisoId(@Param("avisoId") Integer avisoId);
}