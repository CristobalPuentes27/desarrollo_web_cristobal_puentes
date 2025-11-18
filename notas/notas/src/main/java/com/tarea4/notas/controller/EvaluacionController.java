package com.tarea4.notas.controller;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.stream.Collectors;
import com.tarea4.notas.models.AvisoAdopcion;
import com.tarea4.notas.models.Nota;
import com.tarea4.notas.DTO.AvisoConNotaDTO;
import com.tarea4.notas.DTO.EvaluacionRequestDTO;
import com.tarea4.notas.DTO.EvaluacionResponseDTO;
@RestController
@RequestMapping("/api/evaluaciones")
@CrossOrigin(origins = "*") // Para permitir requests desde Flask
public class EvaluacionController {

    @Autowired
    private AvisoAdopcionRepository avisoRepository;
    
    @Autowired
    private NotaRepository notaRepository;

    // GET: Listar todos los avisos con sus promedios de nota
    @GetMapping("/avisos")
    public ResponseEntity<List<AvisoConNotaDTO>> getAvisosConNotas() {
        try {
            List<AvisoAdopcion> avisos = avisoRepository.findAllWithComunaAndRegion();
            
            List<AvisoConNotaDTO> avisosConNotas = avisos.stream().map(aviso -> {
                Double promedio = notaRepository.findPromedioByAvisoId(aviso.getId());
                
                return new AvisoConNotaDTO(
                    aviso.getId(),
                    aviso.getFechaIngreso(),
                    aviso.getSector(),
                    aviso.getCantidad(),
                    aviso.getTipo().name(),
                    aviso.getEdad(),
                    aviso.getComuna().getNombre(),
                    promedio
                );
            }).collect(Collectors.toList());
            
            return ResponseEntity.ok(avisosConNotas);
            
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }

    // POST: Agregar una nueva evaluación
    @PostMapping("/evaluar")
    public ResponseEntity<EvaluacionResponseDTO> agregarEvaluacion(@RequestBody EvaluacionRequestDTO request) {
        try {
            // Validar que la nota esté entre 1 y 7
            if (request.getNota() == null || request.getNota() < 1 || request.getNota() > 7) {
                return ResponseEntity.badRequest().body(
                    new EvaluacionResponseDTO(false, "La nota debe ser un número entre 1 y 7", null)
                );
            }
            
            // Verificar que el aviso existe
            AvisoAdopcion aviso = avisoRepository.findById(request.getAvisoId())
                .orElse(null);
                
            if (aviso == null) {
                return ResponseEntity.badRequest().body(
                    new EvaluacionResponseDTO(false, "El aviso no existe", null)
                );
            }
            
            // Crear y guardar la nueva nota
            Nota nuevaNota = new Nota();
            nuevaNota.setAviso(aviso);
            nuevaNota.setNota(request.getNota());
            notaRepository.save(nuevaNota);
            
            // Calcular nuevo promedio
            Double nuevoPromedio = notaRepository.findPromedioByAvisoId(request.getAvisoId());
            
            return ResponseEntity.ok(new EvaluacionResponseDTO(
                true, 
                "Evaluación agregada exitosamente", 
                nuevoPromedio
            ));
            
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(
                new EvaluacionResponseDTO(false, "Error interno del servidor", null)
            );
        }
    }
}