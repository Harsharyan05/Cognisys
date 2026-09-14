from app.parser.symbol_extractor import SymbolExtractor

extractor = SymbolExtractor()

symbols = extractor.extract("app")

for file, data in symbols.items():

    if data["classes"] or data["functions"]:

        print("=" * 60)

        print(file)

        print(data)