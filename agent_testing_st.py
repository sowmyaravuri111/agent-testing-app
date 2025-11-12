#!/usr/bin/env python
# coding: utf-8

# In[12]:

import os
import streamlit as st
import datetime
from openai import OpenAI

# Initialize client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Streamlit UI
st.title("🧠 AI Agent Testing Dashboard")
st.write("### Running Agent Tests...")

# Define test cases
tests = [
    {"input": "What is 2 + 2?", "expected": "4"},
    {"input": "What is today's date?", "expected": datetime.datetime.now().strftime("%B %d, %Y")},
    {"input": "What color is the sky on a clear day?", "expected": "blue"},
]

results = []

# Run tests
for test in tests:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": test["input"]},
        ],
    )
    agent_output = response.choices[0].message.content.strip()
    passed = test["expected"].lower() in agent_output.lower()

    results.append({
        "Test Input": test["input"],
        "Expected Output": test["expected"],
        "Agent Output": agent_output,
        "Result": "✅ PASS" if passed else "❌ FAIL",
    })

# Display results in table
st.write("### 🧪 Test Results")
st.table(results)

# Summary metrics
passed_count = sum(1 for r in results if "PASS" in r["Result"])
failed_count = len(results) - passed_count

col1, col2, col3 = st.columns(3)
col1.metric("Total Tests", len(results))
col2.metric("Passed", passed_count)
col3.metric("Failed", failed_count)

st.success("✅ Testing complete!") if failed_count == 0 else st.warning("⚠️ Some tests failed.")


# In[ ]:




