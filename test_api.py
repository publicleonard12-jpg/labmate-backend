"""
LabMate AI - API Test Script
Run this to test all endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

def print_section(title):
    """Print section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_endpoint(name, method, endpoint, data=None):
    """Test an API endpoint"""
    print(f"\n🧪 Testing: {name}")
    print(f"   Method: {method} {endpoint}")
    
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        else:
            response = requests.post(url, json=data, timeout=30)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ SUCCESS")
            print(f"   Response preview: {json.dumps(result, indent=2)[:500]}...")
        else:
            print(f"   ❌ FAILED")
            print(f"   Error: {response.text}")
        
        return response
    
    except requests.exceptions.ConnectionError:
        print(f"   ❌ CONNECTION ERROR")
        print(f"   Make sure the server is running: python app.py")
        return None
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return None

def run_tests():
    """Run all API tests"""
    
    print(f"\n{'🚀 LabMate AI - API Test Suite':^60}")
    print(f"{'Starting tests at ' + datetime.now().strftime('%H:%M:%S'):^60}\n")
    
    # Test 1: Health Check
    print_section("1. Health Check")
    test_endpoint(
        "Health Check",
        "GET",
        "/health"
    )
    
    # Test 2: Lab Report Generation
    print_section("2. Lab Report Generator")
    test_endpoint(
        "Generate Lab Report",
        "POST",
        "/api/generate-report",
        {
            "title": "Acid-Base Titration",
            "course_code": "CH 273",
            "objective": "To determine the concentration of HCl solution using standardized NaOH",
            "materials": [
                "Burette (50ml)",
                "Pipette (25ml)",
                "Conical flask",
                "NaOH solution (0.1M)",
                "HCl solution (unknown concentration)",
                "Phenolphthalein indicator"
            ],
            "procedure": "1. Rinse burette with NaOH solution\n2. Fill burette with NaOH to 0.0ml mark\n3. Pipette 25ml HCl into conical flask\n4. Add 2-3 drops of phenolphthalein\n5. Titrate slowly until permanent pink color appears\n6. Record burette reading\n7. Repeat for accuracy",
            "observations": "Initial burette reading: 0.0ml\nFinal burette reading: 24.5ml\nVolume of NaOH used: 24.5ml\nColor change: Colorless to pale pink\nEnd point was sharp and easily observable",
            "data": [
                {"trial": 1, "initial_reading": 0.0, "final_reading": 24.5, "volume_used": 24.5},
                {"trial": 2, "initial_reading": 0.0, "final_reading": 24.3, "volume_used": 24.3},
                {"trial": 3, "initial_reading": 0.0, "final_reading": 24.4, "volume_used": 24.4}
            ]
        }
    )
    
    test_endpoint(
        "Format Raw Notes",
        "POST",
        "/api/format-report",
        {
            "raw_notes": "We heated the copper sulfate solution in a beaker. It turned from blue to white powder when water evaporated. Then we added water back and it turned blue again. This shows that the reaction is reversible.",
            "report_type": "chemistry"
        }
    )
    
    # Test 3: Research Papers
    print_section("3. Research Paper Service")
    test_endpoint(
        "Search Papers",
        "POST",
        "/api/search-papers",
        {
            "query": "chemical thermodynamics entropy",
            "max_results": 5
        }
    )
    
    # Test 4: Video Resources
    print_section("4. Video Resource Finder")
    test_endpoint(
        "Find Videos",
        "POST",
        "/api/find-videos",
        {
            "topic": "organic chemistry reactions",
            "course_code": "CH 257",
            "max_results": 5,
            "difficulty": "intermediate"
        }
    )
    
    test_endpoint(
        "Create Learning Playlist",
        "POST",
        "/api/curate-playlist",
        {
            "course_code": "CH 275",
            "topics": [
                "stoichiometry",
                "limiting reagent",
                "percent yield"
            ]
        }
    )
    
    # Test 5: AI Chat Assistant
    print_section("5. AI Study Assistant")
    test_endpoint(
        "Chat with AI",
        "POST",
        "/api/chat",
        {
            "message": "Explain Le Chatelier's principle with an example",
            "context": "CH 263 - Chemical Thermodynamics"
        }
    )
    
    test_endpoint(
        "Explain Concept",
        "POST",
        "/api/explain-concept",
        {
            "concept": "enthalpy",
            "level": "undergraduate",
            "include_examples": True
        }
    )
    
    test_endpoint(
        "Solve Formula",
        "POST",
        "/api/solve-formula",
        {
            "formula": "PV = nRT",
            "known_values": {
                "P": 101.325,
                "V": 22.4,
                "T": 273.15,
                "R": 8.314
            },
            "solve_for": "n"
        }
    )
    
    # Summary
    print("\n" + "="*60)
    print("  ✅ Test Suite Complete!")
    print("="*60)
    print("\nNext Steps:")
    print("1. Review the test results above")
    print("2. If you see [MOCK RESPONSE], set your GROQ_API_KEY in .env")
    print("3. All endpoints returning 200 = Backend is ready! 🎉")
    print("4. Now you can connect your mobile frontend\n")

if __name__ == "__main__":
    print("\n⚠️  IMPORTANT: Make sure the Flask server is running!")
    print("   Run in another terminal: python app.py\n")
    
    input("Press Enter to start tests...")
    run_tests()
