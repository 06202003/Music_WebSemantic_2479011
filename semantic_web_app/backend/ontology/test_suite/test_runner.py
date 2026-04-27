#!/usr/bin/env python3
"""
Music Ontology Test Runner
Tests all SPARQL queries against the music_runtime.ttl ontology
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json

try:
    from rdflib import Graph
    from rdflib.plugins.sparql import prepareQuery
except ImportError:
    print("ERROR: rdflib not installed. Install with: pip install rdflib")
    sys.exit(1)


class MusicOntologyTester:
    def __init__(self, ontology_path, test_results_path):
        self.ontology_path = ontology_path
        self.test_results_path = test_results_path
        self.graph = None
        self.test_results = []
        self.test_summary = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0
        }
    
    def load_ontology(self):
        """Load the TTL ontology file"""
        print(f"Loading ontology from: {self.ontology_path}")
        try:
            self.graph = Graph()
            self.graph.parse(self.ontology_path, format="turtle")
            print(f"✓ Ontology loaded successfully ({len(self.graph)} triples)")
            return True
        except Exception as e:
            print(f"✗ Failed to load ontology: {e}")
            return False
    
    def load_sparql_queries(self, queries_dir):
        """Load all SPARQL query files"""
        queries = {}
        try:
            for file in sorted(Path(queries_dir).glob("*.sparql")):
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    queries[file.stem] = content
            print(f"✓ Loaded {len(queries)} SPARQL query files")
            return queries
        except Exception as e:
            print(f"✗ Failed to load queries: {e}")
            return {}
    
    def parse_test_blocks(self, content):
        """Extract individual test blocks from SPARQL file"""
        blocks = content.split("\n---\n")
        tests = []
        for block in blocks:
            block = block.strip()
            if block:
                tests.append(block)
        return tests
    
    def execute_query(self, query_text):
        """Execute SPARQL query against the graph"""
        try:
            # Extract query without comments
            lines = [l for l in query_text.split('\n') if not l.strip().startswith('#')]
            clean_query = '\n'.join(lines)
            
            if "ASK" in query_text.upper():
                result = self.graph.query(clean_query)
                return {"type": "ASK", "result": bool(result), "rows": 1}
            elif "SELECT" in query_text.upper():
                result = self.graph.query(clean_query)
                rows = list(result)
                return {"type": "SELECT", "result": rows, "rows": len(rows)}
            elif "CONSTRUCT" in query_text.upper():
                result = self.graph.query(clean_query)
                triples = list(result)
                return {"type": "CONSTRUCT", "result": triples, "rows": len(triples)}
            elif "DESCRIBE" in query_text.upper():
                result = self.graph.query(clean_query)
                results = list(result)
                return {"type": "DESCRIBE", "result": results, "rows": len(results)}
            else:
                return {"error": "Unknown query type"}
        except Exception as e:
            return {"error": str(e)}
    
    def run_tests(self, test_files_dir):
        """Run all test files"""
        print("\n" + "="*70)
        print("STARTING TEST EXECUTION")
        print("="*70)
        
        queries = self.load_sparql_queries(test_files_dir)
        
        for file_name, content in sorted(queries.items()):
            print(f"\n{'─'*70}")
            print(f"Testing: {file_name}")
            print(f"{'─'*70}")
            
            test_blocks = self.parse_test_blocks(content)
            
            for i, query_block in enumerate(test_blocks, 1):
                self.test_summary["total"] += 1
                
                try:
                    result = self.execute_query(query_block)
                    
                    if "error" in result:
                        status = "✗ ERROR"
                        self.test_summary["errors"] += 1
                    else:
                        # For basic validation, just check if result is returned
                        status = "✓ PASS"
                        self.test_summary["passed"] += 1
                    
                    print(f"  Test {i}: {status}")
                    print(f"    Type: {result.get('type', 'Unknown')}")
                    print(f"    Rows: {result.get('rows', 0)}")
                    if "error" in result:
                        print(f"    Error: {result['error']}")
                    
                    self.test_results.append({
                        "file": file_name,
                        "test": i,
                        "status": status,
                        "result": result
                    })
                    
                except Exception as e:
                    print(f"  Test {i}: ✗ EXCEPTION")
                    print(f"    Error: {str(e)}")
                    self.test_summary["failed"] += 1
                    self.test_results.append({
                        "file": file_name,
                        "test": i,
                        "status": "✗ FAILED",
                        "error": str(e)
                    })
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        
        total = self.test_summary["total"]
        passed = self.test_summary["passed"]
        failed = self.test_summary["failed"]
        errors = self.test_summary["errors"]
        
        print(f"Total Tests:    {total}")
        print(f"Passed:         {passed} ✓")
        print(f"Failed:         {failed} ✗")
        print(f"Errors:         {errors} ⚠")
        
        if total > 0:
            pass_rate = (passed / total) * 100
            print(f"Pass Rate:      {pass_rate:.1f}%")
        
        print("="*70)
        
        if passed == total:
            print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        elif passed >= total * 0.8:
            print("⚠ Most tests passed, some issues detected")
        else:
            print("✗ Significant test failures detected")
    
    def save_results(self):
        """Save results to JSON"""
        results_data = {
            "timestamp": datetime.now().isoformat(),
            "ontology": str(self.ontology_path),
            "summary": self.test_summary,
            "test_results": self.test_results
        }
        
        json_path = self.test_results_path.replace(".md", ".json")
        try:
            with open(json_path, 'w') as f:
                json.dump(results_data, f, indent=2)
            print(f"\n✓ Results saved to: {json_path}")
        except Exception as e:
            print(f"\n✗ Failed to save results: {e}")
    
    def run(self, queries_dir):
        """Main test runner"""
        print("\n" + "="*70)
        print("MUSIC ONTOLOGY TEST RUNNER")
        print("="*70)
        print(f"Ontology: {self.ontology_path}")
        print(f"Queries:  {queries_dir}")
        print("="*70 + "\n")
        
        if not self.load_ontology():
            return False
        
        self.run_tests(queries_dir)
        self.print_summary()
        self.save_results()
        
        return self.test_summary["failed"] == 0


def main():
    # Get script directory
    script_dir = Path(__file__).parent
    
    # Paths
    ontology_file = script_dir.parent / "music_runtime.ttl"
    queries_dir = script_dir / "sparql_queries"
    results_file = script_dir / "test_results.md"
    
    # Verify paths exist
    if not ontology_file.exists():
        print(f"ERROR: Ontology file not found: {ontology_file}")
        return 1
    
    if not queries_dir.exists():
        print(f"ERROR: Queries directory not found: {queries_dir}")
        return 1
    
    # Run tests
    tester = MusicOntologyTester(str(ontology_file), str(results_file))
    success = tester.run(str(queries_dir))
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
