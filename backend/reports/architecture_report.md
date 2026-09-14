# Cognisys Architecture Report

## Architecture Patterns

### Layered Architecture
- Confidence: 0.95
- Evidence:
  - Business layer detected
  - Persistence layer detected
  - Presentation layer detected

### MVC
- Confidence: 0.60
- Evidence:
  - Presentation layer detected
  - Persistence layer detected

### Monolithic Architecture
- Confidence: 0.85
- Evidence:
  - 105 modules detected
  - Single deployable project

## Hotspots

- **app.ai.embedding_models** (Score: 10, Risk: HIGH)
- **app.ai.llm_engine** (Score: 8, Risk: MEDIUM)
- **app.architecture.architecture_engine** (Score: 8, Risk: MEDIUM)
- **app.graph.graph_models** (Score: 8, Risk: MEDIUM)
- **app.ai.multi_vector_store** (Score: 7, Risk: MEDIUM)
- **app.ai.rag_pipeline** (Score: 7, Risk: MEDIUM)
- **app.architecture.report_generator** (Score: 7, Risk: MEDIUM)
- **app.services.repository_service** (Score: 7, Risk: MEDIUM)
- **app.ai.embedding_generator** (Score: 6, Risk: MEDIUM)
- **app.ai.hybrid_retriever** (Score: 6, Risk: MEDIUM)
- **app.ai.vector_store** (Score: 6, Risk: MEDIUM)
- **app.main** (Score: 5, Risk: MEDIUM)
- **app.ai.citation_engine** (Score: 5, Risk: MEDIUM)
- **app.ai.knowledge_document_generator** (Score: 5, Risk: MEDIUM)
- **app.ai.multi_semantic_search** (Score: 5, Risk: MEDIUM)
- **app.architecture.architecture_models** (Score: 5, Risk: MEDIUM)
- **app.architecture.dependency_graph** (Score: 5, Risk: MEDIUM)
- **app.architecture.hotspot_detector** (Score: 5, Risk: MEDIUM)
- **app.architecture.recommendation_engine** (Score: 5, Risk: MEDIUM)
- **app.parser.repository_cloner** (Score: 5, Risk: MEDIUM)
- **app.parser.technology_detector** (Score: 5, Risk: MEDIUM)
- **app.services.analysis_service** (Score: 5, Risk: MEDIUM)
- **app.services.knowledge_graph_service** (Score: 5, Risk: MEDIUM)
- **app.api.v1.analysis** (Score: 5, Risk: MEDIUM)
- **app.ai.multi_embedding_generator** (Score: 4, Risk: LOW)
- **app.ai.performance_monitor** (Score: 4, Risk: LOW)
- **app.ai.prompt_builder_v3** (Score: 4, Risk: LOW)
- **app.ai.query_classifier** (Score: 4, Risk: LOW)
- **app.api.router** (Score: 4, Risk: LOW)
- **app.architecture.service_detector** (Score: 4, Risk: LOW)
- **app.core.logger** (Score: 4, Risk: LOW)
- **app.graph.entity_extractor** (Score: 4, Risk: LOW)
- **app.graph.graph_builder** (Score: 4, Risk: LOW)
- **app.parser.dependency_analyzer** (Score: 4, Risk: LOW)
- **app.api.v1.repository** (Score: 4, Risk: LOW)
- **list_models** (Score: 3, Risk: LOW)
- **app.ai.answer_formatter** (Score: 3, Risk: LOW)
- **app.ai.chunker** (Score: 3, Risk: LOW)
- **app.ai.chunk_models** (Score: 3, Risk: LOW)
- **app.ai.conversation_memory** (Score: 3, Risk: LOW)
- **app.ai.document_generator** (Score: 3, Risk: LOW)
- **app.ai.multi_document_chunker** (Score: 3, Risk: LOW)
- **app.ai.repository_overview_generator** (Score: 3, Risk: LOW)
- **app.ai.semantic_search** (Score: 3, Risk: LOW)
- **app.architecture.architecture_pattern_detector** (Score: 3, Risk: LOW)
- **app.architecture.layer_detector** (Score: 3, Risk: LOW)
- **app.architecture.recommendation_models** (Score: 3, Risk: LOW)
- **app.core.config** (Score: 3, Risk: LOW)
- **app.database.db** (Score: 3, Risk: LOW)
- **app.graph.relationship_extractor** (Score: 3, Risk: LOW)
- **app.parser.architecture_analyzer** (Score: 3, Risk: LOW)
- **app.parser.file_classifier** (Score: 3, Risk: LOW)
- **app.parser.import_graph_builder** (Score: 3, Risk: LOW)
- **app.parser.python_ast_parser** (Score: 3, Risk: LOW)
- **app.parser.repository_scanner** (Score: 3, Risk: LOW)
- **app.parser.symbol_extractor** (Score: 3, Risk: LOW)
- **app.schemas.analysis** (Score: 3, Risk: LOW)
- **app.schemas.repository** (Score: 3, Risk: LOW)
- **app.ai.prompt_builder_v2** (Score: 2, Risk: LOW)
- **app.architecture.circular_dependency_detector** (Score: 2, Risk: LOW)
- **app.architecture.entry_point_detector** (Score: 2, Risk: LOW)
- **app.core.constants** (Score: 2, Risk: LOW)
- **app.database.session** (Score: 2, Risk: LOW)
- **app.graph.graph_serializer** (Score: 2, Risk: LOW)
- **app.parser.call_graph_builder** (Score: 2, Risk: LOW)
- **app.ai.prompt_builder** (Score: 1, Risk: LOW)
- **app.models.repository_metadeta** (Score: 1, Risk: LOW)
- **app.ai.chat** (Score: 0, Risk: LOW)
- **app.ai.llm** (Score: 0, Risk: LOW)
- **app.ai.prompt_templates** (Score: 0, Risk: LOW)
- **app.ai.reasoning** (Score: 0, Risk: LOW)
- **app.database.models** (Score: 0, Risk: LOW)
- **app.graph.blast_radius** (Score: 0, Risk: LOW)
- **app.graph.graph_utils** (Score: 0, Risk: LOW)
- **app.security.dependency_checker** (Score: 0, Risk: LOW)
- **app.security.permission_checker** (Score: 0, Risk: LOW)
- **app.security.report_generator** (Score: 0, Risk: LOW)
- **app.security.secret_scanner** (Score: 0, Risk: LOW)
- **app.services.analyze_repository** (Score: 0, Risk: LOW)
- **app.services.generate_report** (Score: 0, Risk: LOW)
- **app.workflows.github_actions** (Score: 0, Risk: LOW)
- **app.workflows.trigger_parser** (Score: 0, Risk: LOW)
- **app.workflows.workflow_graph** (Score: 0, Risk: LOW)
- **app.api.v1.chat** (Score: 0, Risk: LOW)
- **app.api.v1.graph** (Score: 0, Risk: LOW)
- **app.api.v1.security** (Score: 0, Risk: LOW)
- **app.api.v1.workflow** (Score: 0, Risk: LOW)
- **app.ai.providers.base** (Score: 0, Risk: LOW)
- **app.ai.providers.gemini_provider** (Score: 0, Risk: LOW)
- **app.ai.providers.ollama_provider** (Score: 0, Risk: LOW)
- **app.ai.providers.openai_provider** (Score: 0, Risk: LOW)

## Circular Dependencies

No circular dependencies detected.

## Recommendations

### High Coupling Detected
- Priority: HIGH
- Module: app.ai.embedding_models
- Recommendation: Split this module into smaller services to reduce coupling.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.llm_engine
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.architecture.architecture_engine
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.graph.graph_models
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.multi_vector_store
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.rag_pipeline
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.architecture.report_generator
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.services.repository_service
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.embedding_generator
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.hybrid_retriever
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.vector_store
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.main
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.citation_engine
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.knowledge_document_generator
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.multi_semantic_search
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.architecture.architecture_models
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.architecture.dependency_graph
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.architecture.hotspot_detector
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.architecture.recommendation_engine
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.parser.repository_cloner
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.parser.technology_detector
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.services.analysis_service
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.services.knowledge_graph_service
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.api.v1.analysis
- Recommendation: Consider refactoring this module if it continues to grow.

### Architecture Pattern
- Priority: LOW
- Module: Repository
- Recommendation: Layered architecture detected. Continue enforcing layer separation.

### Scalability
- Priority: LOW
- Module: Repository
- Recommendation: Consider modularization or microservices as the project grows.

