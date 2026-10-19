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
  - 263 modules detected
  - Single deployable project

## Hotspots

- **app.ai.embedding_models** (Score: 21, Risk: HIGH)
- **app.api.v1.intelligence** (Score: 14, Risk: HIGH)
- **app.services.repository_service** (Score: 13, Risk: HIGH)
- **storage.temp.Cognisys.backend.app.api.v1.intelligence** (Score: 12, Risk: HIGH)
- **app.ai.multi_vector_store** (Score: 12, Risk: HIGH)
- **app.ai.repository_indexer** (Score: 12, Risk: HIGH)
- **app.architecture.architecture_engine** (Score: 12, Risk: HIGH)
- **app.ai.rag_pipeline** (Score: 11, Risk: HIGH)
- **app.graph.graph_models** (Score: 11, Risk: HIGH)
- **app.ai.hybrid_retriever** (Score: 10, Risk: HIGH)
- **app.ai.llm_engine** (Score: 9, Risk: MEDIUM)
- **app.api.v1.chat** (Score: 9, Risk: MEDIUM)
- **storage.temp.Cognisys.backend.app.architecture.architecture_engine** (Score: 8, Risk: MEDIUM)
- **app.ai.symbol_semantic_search** (Score: 8, Risk: MEDIUM)
- **app.architecture.architecture_models** (Score: 8, Risk: MEDIUM)
- **app.architecture.hotspot_detector** (Score: 8, Risk: MEDIUM)
- **app.architecture.report_generator** (Score: 8, Risk: MEDIUM)
- **app.parser.technology_detector** (Score: 8, Risk: MEDIUM)
- **app.repository.repository_manager** (Score: 8, Risk: MEDIUM)
- **storage.temp.Cognisys.backend.app.ai.hybrid_retriever** (Score: 7, Risk: MEDIUM)
- **storage.temp.Cognisys.backend.app.ai.llm_engine** (Score: 7, Risk: MEDIUM)
- **storage.temp.Cognisys.backend.app.ai.rag_pipeline** (Score: 7, Risk: MEDIUM)
- **storage.temp.Cognisys.backend.app.ai.repository_indexer** (Score: 7, Risk: MEDIUM)
- **storage.temp.Cognisys.backend.app.api.v1.chat** (Score: 7, Risk: MEDIUM)
- **app.ai.citation_engine** (Score: 7, Risk: MEDIUM)
- **app.ai.vector_store** (Score: 7, Risk: MEDIUM)
- **app.api.router** (Score: 7, Risk: MEDIUM)
- **app.architecture.dependency_graph** (Score: 7, Risk: MEDIUM)
- **app.intelligence.intelligence_engine** (Score: 7, Risk: MEDIUM)
- **app.services.analysis_service** (Score: 7, Risk: MEDIUM)
- **storage.temp.Cognisys.backend.app.ai.embedding_generator** (Score: 6, Risk: MEDIUM)
- **storage.temp.Cognisys.backend.app.ai.multi_vector_store** (Score: 6, Risk: MEDIUM)
- **storage.temp.Cognisys.backend.app.ai.symbol_semantic_search** (Score: 6, Risk: MEDIUM)
- **storage.temp.Cognisys.backend.app.architecture.report_generator** (Score: 6, Risk: MEDIUM)
- **app.ai.embedding_generator** (Score: 6, Risk: MEDIUM)
- **app.ai.multi_semantic_search** (Score: 6, Risk: MEDIUM)
- **app.ai.symbol_embedding_indexer** (Score: 6, Risk: MEDIUM)
- **app.architecture.recommendation_engine** (Score: 6, Risk: MEDIUM)
- **app.core.logger** (Score: 6, Risk: MEDIUM)
- **app.parser.dependency_analyzer** (Score: 6, Risk: MEDIUM)
- **app.parser.repository_cloner** (Score: 6, Risk: MEDIUM)
- **app.api.v1.analysis** (Score: 6, Risk: MEDIUM)
- **app.main** (Score: 5, Risk: MEDIUM)
- **storage.temp.Cognisys.backend.app.main** (Score: 5, Risk: MEDIUM)
- **storage.temp.Cognisys.backend.app.ai.knowledge_document_generator** (Score: 5, Risk: MEDIUM)
- **storage.temp.Cognisys.backend.app.ai.vector_store** (Score: 5, Risk: MEDIUM)
- **storage.temp.Cognisys.backend.app.api.router** (Score: 5, Risk: MEDIUM)
- **storage.temp.Cognisys.backend.app.intelligence.intelligence_engine** (Score: 5, Risk: MEDIUM)
- **storage.temp.Cognisys.backend.app.services.analysis_service** (Score: 5, Risk: MEDIUM)
- **storage.temp.Cognisys.backend.app.services.knowledge_graph_service** (Score: 5, Risk: MEDIUM)
- **storage.temp.Cognisys.backend.app.services.repository_service** (Score: 5, Risk: MEDIUM)
- **app.ai.answer_formatter** (Score: 5, Risk: MEDIUM)
- **app.ai.chunk_models** (Score: 5, Risk: MEDIUM)
- **app.ai.knowledge_document_generator** (Score: 5, Risk: MEDIUM)
- **app.ai.performance_monitor** (Score: 5, Risk: MEDIUM)
- **app.ai.prompt_builder_v3** (Score: 5, Risk: MEDIUM)
- **app.ai.query_classifier** (Score: 5, Risk: MEDIUM)
- **app.architecture.recommendation_models** (Score: 5, Risk: MEDIUM)
- **app.architecture.service_detector** (Score: 5, Risk: MEDIUM)
- **app.core.config** (Score: 5, Risk: MEDIUM)
- **app.graph.code_graph_engine** (Score: 5, Risk: MEDIUM)
- **app.graph.graph_builder** (Score: 5, Risk: MEDIUM)
- **app.parser.architecture_analyzer** (Score: 5, Risk: MEDIUM)
- **app.parser.repository_scanner** (Score: 5, Risk: MEDIUM)
- **app.services.knowledge_graph_service** (Score: 5, Risk: MEDIUM)
- **app.api.v1.repository** (Score: 5, Risk: MEDIUM)
- **debug_retrieval** (Score: 4, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.multi_embedding_generator** (Score: 4, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.multi_semantic_search** (Score: 4, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.symbol_embedding_indexer** (Score: 4, Risk: LOW)
- **storage.temp.Cognisys.backend.app.architecture.recommendation_engine** (Score: 4, Risk: LOW)
- **storage.temp.Cognisys.backend.app.parser.repository_cloner** (Score: 4, Risk: LOW)
- **storage.temp.Cognisys.backend.app.repository.repository_manager** (Score: 4, Risk: LOW)
- **storage.temp.Cognisys.backend.app.api.v1.analysis** (Score: 4, Risk: LOW)
- **app.ai.conversation_memory** (Score: 4, Risk: LOW)
- **app.ai.multi_embedding_generator** (Score: 4, Risk: LOW)
- **app.ai.repository_overview_generator** (Score: 4, Risk: LOW)
- **app.ai.symbol_indexer** (Score: 4, Risk: LOW)
- **app.architecture.architecture_pattern_detector** (Score: 4, Risk: LOW)
- **app.architecture.layer_detector** (Score: 4, Risk: LOW)
- **app.database.db** (Score: 4, Risk: LOW)
- **app.impact.impact_analyzer** (Score: 4, Risk: LOW)
- **app.impact.impact_engine** (Score: 4, Risk: LOW)
- **app.parser.file_classifier** (Score: 4, Risk: LOW)
- **app.parser.import_graph_builder** (Score: 4, Risk: LOW)
- **app.parser.python_ast_parser** (Score: 4, Risk: LOW)
- **app.parser.symbol_extractor** (Score: 4, Risk: LOW)
- **app.parser.symbol_relationship_extractor** (Score: 4, Risk: LOW)
- **app.schemas.analysis** (Score: 4, Risk: LOW)
- **app.schemas.intelligence** (Score: 4, Risk: LOW)
- **app.schemas.repository** (Score: 4, Risk: LOW)
- **list_models** (Score: 3, Risk: LOW)
- **storage.temp.Cognisys.backend.list_models** (Score: 3, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.answer_formatter** (Score: 3, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.chunker** (Score: 3, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.citation_engine** (Score: 3, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.document_generator** (Score: 3, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.embedding_models** (Score: 3, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.multi_document_chunker** (Score: 3, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.performance_monitor** (Score: 3, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.prompt_builder_v3** (Score: 3, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.query_classifier** (Score: 3, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.semantic_search** (Score: 3, Risk: LOW)
- **storage.temp.Cognisys.backend.app.architecture.dependency_graph** (Score: 3, Risk: LOW)
- **storage.temp.Cognisys.backend.app.architecture.service_detector** (Score: 3, Risk: LOW)
- **storage.temp.Cognisys.backend.app.graph.code_graph_engine** (Score: 3, Risk: LOW)
- **storage.temp.Cognisys.backend.app.graph.entity_extractor** (Score: 3, Risk: LOW)
- **storage.temp.Cognisys.backend.app.graph.graph_models** (Score: 3, Risk: LOW)
- **storage.temp.Cognisys.backend.app.api.v1.repository** (Score: 3, Risk: LOW)
- **app.ai.architecture_citation_engine** (Score: 3, Risk: LOW)
- **app.ai.chunker** (Score: 3, Risk: LOW)
- **app.ai.document_generator** (Score: 3, Risk: LOW)
- **app.ai.multi_document_chunker** (Score: 3, Risk: LOW)
- **app.ai.semantic_search** (Score: 3, Risk: LOW)
- **app.architecture.circular_dependency_detector** (Score: 3, Risk: LOW)
- **app.core.constants** (Score: 3, Risk: LOW)
- **app.graph.entity_extractor** (Score: 3, Risk: LOW)
- **app.graph.graph_serializer** (Score: 3, Risk: LOW)
- **app.intelligence.query_classifier** (Score: 3, Risk: LOW)
- **app.schemas.chat** (Score: 3, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.conversation_memory** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.prompt_builder_v2** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.repository_overview_generator** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.symbol_indexer** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.architecture.architecture_models** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.architecture.architecture_pattern_detector** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.architecture.entry_point_detector** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.architecture.hotspot_detector** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.architecture.layer_detector** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.core.logger** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.database.db** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.database.session** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.graph.relationship_extractor** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.impact.impact_analyzer** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.impact.impact_engine** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.parser.call_graph_builder** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.parser.dependency_analyzer** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.parser.file_classifier** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.parser.import_graph_builder** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.parser.python_ast_parser** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.parser.symbol_extractor** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.parser.symbol_relationship_extractor** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.parser.technology_detector** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.schemas.analysis** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.schemas.intelligence** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.schemas.repository** (Score: 2, Risk: LOW)
- **app.ai.prompt_builder_v2** (Score: 2, Risk: LOW)
- **app.architecture.entry_point_detector** (Score: 2, Risk: LOW)
- **app.database.session** (Score: 2, Risk: LOW)
- **app.graph.code_graph** (Score: 2, Risk: LOW)
- **app.graph.graph_aware_query** (Score: 2, Risk: LOW)
- **app.graph.graph_query** (Score: 2, Risk: LOW)
- **app.graph.relationship_extractor** (Score: 2, Risk: LOW)
- **app.intelligence.architecture_aware_retriever** (Score: 2, Risk: LOW)
- **app.intelligence.architecture_context** (Score: 2, Risk: LOW)
- **app.intelligence.unified_context** (Score: 2, Risk: LOW)
- **app.parser.call_graph_builder** (Score: 2, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.architecture_citation_engine** (Score: 1, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.chunk_models** (Score: 1, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.prompt_builder** (Score: 1, Risk: LOW)
- **storage.temp.Cognisys.backend.app.architecture.circular_dependency_detector** (Score: 1, Risk: LOW)
- **storage.temp.Cognisys.backend.app.architecture.recommendation_models** (Score: 1, Risk: LOW)
- **storage.temp.Cognisys.backend.app.core.config** (Score: 1, Risk: LOW)
- **storage.temp.Cognisys.backend.app.core.constants** (Score: 1, Risk: LOW)
- **storage.temp.Cognisys.backend.app.graph.graph_builder** (Score: 1, Risk: LOW)
- **storage.temp.Cognisys.backend.app.graph.graph_serializer** (Score: 1, Risk: LOW)
- **storage.temp.Cognisys.backend.app.intelligence.query_classifier** (Score: 1, Risk: LOW)
- **storage.temp.Cognisys.backend.app.models.repository_metadeta** (Score: 1, Risk: LOW)
- **storage.temp.Cognisys.backend.app.parser.architecture_analyzer** (Score: 1, Risk: LOW)
- **storage.temp.Cognisys.backend.app.parser.repository_scanner** (Score: 1, Risk: LOW)
- **storage.temp.Cognisys.backend.app.schemas.chat** (Score: 1, Risk: LOW)
- **app.ai.prompt_builder** (Score: 1, Risk: LOW)
- **app.models.repository_metadeta** (Score: 1, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.chat** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.llm** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.prompt_templates** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.reasoning** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.symbol_relationship_index** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.database.models** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.graph.blast_radius** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.graph.code_graph** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.graph.graph_aware_query** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.graph.graph_query** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.graph.graph_utils** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.intelligence.architecture_aware_retriever** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.intelligence.architecture_context** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.intelligence.graph_aware_query** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.intelligence.unified_context** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.security.dependency_checker** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.security.permission_checker** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.security.report_generator** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.security.secret_scanner** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.services.analyze_repository** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.services.generate_report** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.workflows.github_actions** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.workflows.trigger_parser** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.workflows.workflow_graph** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.api.v1.graph** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.api.v1.security** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.api.v1.workflow** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.providers.base** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.providers.gemini_provider** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.providers.ollama_provider** (Score: 0, Risk: LOW)
- **storage.temp.Cognisys.backend.app.ai.providers.openai_provider** (Score: 0, Risk: LOW)
- **app.ai.chat** (Score: 0, Risk: LOW)
- **app.ai.llm** (Score: 0, Risk: LOW)
- **app.ai.prompt_templates** (Score: 0, Risk: LOW)
- **app.ai.reasoning** (Score: 0, Risk: LOW)
- **app.ai.symbol_relationship_index** (Score: 0, Risk: LOW)
- **app.database.models** (Score: 0, Risk: LOW)
- **app.graph.blast_radius** (Score: 0, Risk: LOW)
- **app.graph.graph_utils** (Score: 0, Risk: LOW)
- **app.intelligence.graph_aware_query** (Score: 0, Risk: LOW)
- **app.security.dependency_checker** (Score: 0, Risk: LOW)
- **app.security.permission_checker** (Score: 0, Risk: LOW)
- **app.security.report_generator** (Score: 0, Risk: LOW)
- **app.security.secret_scanner** (Score: 0, Risk: LOW)
- **app.services.analyze_repository** (Score: 0, Risk: LOW)
- **app.services.generate_report** (Score: 0, Risk: LOW)
- **app.workflows.github_actions** (Score: 0, Risk: LOW)
- **app.workflows.trigger_parser** (Score: 0, Risk: LOW)
- **app.workflows.workflow_graph** (Score: 0, Risk: LOW)
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

### High Coupling Detected
- Priority: HIGH
- Module: app.api.v1.intelligence
- Recommendation: Split this module into smaller services to reduce coupling.

### High Coupling Detected
- Priority: HIGH
- Module: app.services.repository_service
- Recommendation: Split this module into smaller services to reduce coupling.

### High Coupling Detected
- Priority: HIGH
- Module: storage.temp.Cognisys.backend.app.api.v1.intelligence
- Recommendation: Split this module into smaller services to reduce coupling.

### High Coupling Detected
- Priority: HIGH
- Module: app.ai.multi_vector_store
- Recommendation: Split this module into smaller services to reduce coupling.

### High Coupling Detected
- Priority: HIGH
- Module: app.ai.repository_indexer
- Recommendation: Split this module into smaller services to reduce coupling.

### High Coupling Detected
- Priority: HIGH
- Module: app.architecture.architecture_engine
- Recommendation: Split this module into smaller services to reduce coupling.

### High Coupling Detected
- Priority: HIGH
- Module: app.ai.rag_pipeline
- Recommendation: Split this module into smaller services to reduce coupling.

### High Coupling Detected
- Priority: HIGH
- Module: app.graph.graph_models
- Recommendation: Split this module into smaller services to reduce coupling.

### High Coupling Detected
- Priority: HIGH
- Module: app.ai.hybrid_retriever
- Recommendation: Split this module into smaller services to reduce coupling.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.llm_engine
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.api.v1.chat
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: storage.temp.Cognisys.backend.app.architecture.architecture_engine
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.symbol_semantic_search
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.architecture.architecture_models
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.architecture.hotspot_detector
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.architecture.report_generator
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.parser.technology_detector
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.repository.repository_manager
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: storage.temp.Cognisys.backend.app.ai.hybrid_retriever
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: storage.temp.Cognisys.backend.app.ai.llm_engine
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: storage.temp.Cognisys.backend.app.ai.rag_pipeline
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: storage.temp.Cognisys.backend.app.ai.repository_indexer
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: storage.temp.Cognisys.backend.app.api.v1.chat
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.citation_engine
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.vector_store
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.api.router
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.architecture.dependency_graph
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.intelligence.intelligence_engine
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.services.analysis_service
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: storage.temp.Cognisys.backend.app.ai.embedding_generator
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: storage.temp.Cognisys.backend.app.ai.multi_vector_store
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: storage.temp.Cognisys.backend.app.ai.symbol_semantic_search
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: storage.temp.Cognisys.backend.app.architecture.report_generator
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.embedding_generator
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.multi_semantic_search
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.symbol_embedding_indexer
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.architecture.recommendation_engine
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.core.logger
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.parser.dependency_analyzer
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.parser.repository_cloner
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.api.v1.analysis
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.main
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: storage.temp.Cognisys.backend.app.main
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: storage.temp.Cognisys.backend.app.ai.knowledge_document_generator
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: storage.temp.Cognisys.backend.app.ai.vector_store
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: storage.temp.Cognisys.backend.app.api.router
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: storage.temp.Cognisys.backend.app.intelligence.intelligence_engine
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: storage.temp.Cognisys.backend.app.services.analysis_service
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: storage.temp.Cognisys.backend.app.services.knowledge_graph_service
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: storage.temp.Cognisys.backend.app.services.repository_service
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.answer_formatter
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.chunk_models
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.knowledge_document_generator
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.performance_monitor
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.prompt_builder_v3
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.ai.query_classifier
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.architecture.recommendation_models
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.architecture.service_detector
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.core.config
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.graph.code_graph_engine
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.graph.graph_builder
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.parser.architecture_analyzer
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.parser.repository_scanner
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.services.knowledge_graph_service
- Recommendation: Consider refactoring this module if it continues to grow.

### Medium Coupling
- Priority: MEDIUM
- Module: app.api.v1.repository
- Recommendation: Consider refactoring this module if it continues to grow.

### Architecture Pattern
- Priority: LOW
- Module: Repository
- Recommendation: Layered architecture detected. Continue enforcing layer separation.

### Scalability
- Priority: LOW
- Module: Repository
- Recommendation: Consider modularization or microservices as the project grows.

