## Test Questions

After starting the application, try the following questions to verify that the RAG pipeline is working correctly.

---

### 1. Direct Retrieval Test

**Question:**

```text
What is the company's top priority?
```

**Expected Answer:**

```text
Protecting the health and safety of every employee, visitor and contractor.
```

---

### 2. STOP Principle Test

**Questions:**

```text
What is the STOP principle?
```

or

```text
Explain the STOP principle used by the company.
```

**Expected Answer:**

```text
S = Elimination
T = Technical measures
O = Organizational measures
P = Personal protective equipment
```

---

### 3. Environmental Policy Test

**Question:**

```text
How does the company contribute to environmental protection?
```

**Expected Result:**

The answer should mention the company's environmental protection measures, sustainability efforts, or environmental responsibilities described in the PDF.

---

### 4. Information Security Test

**Question:**

```text
What are the main goals of information security?
```

**Expected Keywords:**

```text
Confidentiality
Integrity
Availability
```

---

### 5. Diversity Test

**Question:**

```text
Does the company tolerate discrimination?
```

**Expected Answer:**

```text
No.

The company does not tolerate discrimination,
stigmatisation, violence or coercion.
```

---

## Validation Checklist

✅ Direct information retrieval works

✅ STOP principle is correctly retrieved

✅ Environmental policy information is found

✅ Information security concepts are returned

✅ Diversity and anti-discrimination policy is retrieved

✅ End-to-end RAG pipeline is functioning correctly