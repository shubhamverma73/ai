/* ==========================================
   RAG Interview Master
   data.js (Part 1)
   Questions 1–10
========================================== */

const questions = [

   {
      id: 1,
      part: 1,
      question: "अगर 100 Pages की PDF में उत्तर केवल Page 2 पर हो और User वही प्रश्न पूछे, तो क्या Retrieval Accuracy Page Number की वजह से प्रभावित होगी?",

      answer: `
<h3>उत्तर</h3>

<p><b>नहीं।</b></p>

<p>
Vector Database कभी भी Page Number देखकर Search नहीं करता।
वह केवल Semantic Similarity (Meaning) के आधार पर Search करता है।
</p>

<p>
जब PDF को Chunk किया जाता है तो प्रत्येक Chunk का Embedding बनाया जाता है।
User Query का भी Embedding बनता है।
फिर दोनों Embeddings की Similarity Compare की जाती है।
</p>

<p>
इसलिए जानकारी चाहे Page 2 पर हो,
Page 50 पर हो,
या Page 98 पर,
सभी के Retrieve होने की संभावना समान होती है।
</p>

<p><b>Exception:</b></p>

<ul>

<li>Chunking गलत हो।</li>

<li>Relevant Information कई Chunks में टूट गई हो।</li>

<li>Embedding Quality खराब हो।</li>

</ul>

<b>Interview Answer</b>

<p>
Retrieval Page Number के आधार पर नहीं बल्कि Semantic Similarity के आधार पर होता है।
</p>
`
   },

   {
      id: 2,
      part: 1,
      question: "200 Tokens और 1000 Tokens के Chunk Size में कौन सा बेहतर है?",

      answer: `

<h3>उत्तर</h3>

<p>
इसका कोई Fixed Answer नहीं है।
यह पूरी तरह Use Case पर निर्भर करता है।
</p>

<b>200 Token Chunk</b>

<ul>

<li>High Precision</li>

<li>कम Noise</li>

<li>लेकिन Context टूट सकता है।</li>

</ul>

<b>1000 Token Chunk</b>

<ul>

<li>Context अच्छा रहेगा।</li>

<li>लेकिन Extra Information आएगी।</li>

<li>Embedding Generic हो सकती है।</li>

</ul>

<p>

Production Systems सामान्यतः

300–600 Tokens

और

50–100 Token Overlap

Use करते हैं।

</p>

<b>Interview Answer</b>

<p>

Chunk Size हमेशा Context और Precision के बीच Trade-off होता है।

</p>

`
   },

   {
      id: 3,
      part: 1,
      question: "Chunk Overlap क्यों रखा जाता है? 0 Overlap क्यों नहीं?",

      answer: `

<h3>उत्तर</h3>

<p>

अगर Sentence दो Chunks में टूट जाए तो दोनों Chunks अधूरे हो सकते हैं।

</p>

<b>Example</b>

<pre>

Chunk 1

Python is a High Level...

Chunk 2

...Programming Language developed by Guido.

</pre>

<p>

अब किसी भी Chunk में पूरी Information नहीं है।

</p>

<p>

Overlap रखने से दोनों Chunks में थोड़ा Common Context रहता है।

</p>

<b>Interview Answer</b>

<p>

Overlap Chunk Boundary पर Context टूटने से बचाता है।

</p>

`
   },

   {
      id: 4,
      part: 1,
      question: "पूरा एक Page ही एक Chunk क्यों नहीं बना देते?",

      answer: `

<h3>उत्तर</h3>

<p>

अगर पूरा Page Embed करेंगे

तो Embedding बहुत Generic बन जाएगी।

</p>

<p>

Example

Page में

PHP

Python

Java

Docker

Linux

AWS

सब कुछ लिखा है।

</p>

<p>

User पूछे

Docker

तो पूरा Page Retrieve होगा।

जिसमें बहुत Noise होगा।

</p>

<b>Interview Answer</b>

<p>

बहुत बड़े Chunks Retrieval Precision कम कर देते हैं।

</p>

`
   },

   {
      id: 5,
      part: 1,
      question: "अगर एक ही Paragraph PDF में 10 बार लिखा हो तो क्या समस्या होगी?",

      answer: `

<h3>उत्तर</h3>

<p>

Retriever बार-बार वही Chunk Return कर सकता है।

</p>

<p>

Example

Top 5 Results

सभी एक जैसे Paragraph हों।

</p>

<p>

LLM को नया Context नहीं मिलेगा।

</p>

<b>Solution</b>

<ul>

<li>Deduplication</li>

<li>MMR Retrieval</li>

<li>Reranking</li>

</ul>

<b>Interview Answer</b>

<p>

Duplicate Chunks Retrieval Diversity कम कर देते हैं।

</p>

`
   },

   {
      id: 6,
      part: 1,
      question: "अगर PDF में केवल Tables हों तो क्या Normal Chunking सही काम करेगी?",

      answer: `

<h3>उत्तर</h3>

<p>

हमेशा नहीं।

</p>

<p>

Normal Parser कई बार Table का Structure खराब कर देता है।

</p>

<pre>

Name Salary

Amit 50000

Ravi 70000

</pre>

<p>

ऐसे में Embedding भी खराब बन सकती है।

</p>

<b>Solution</b>

<ul>

<li>Table Extraction</li>

<li>Layout Parsing</li>

<li>OCR (यदि Scan हो)</li>

</ul>

<b>Interview Answer</b>

<p>

Tables के लिए Structure Preserve करना जरूरी है।

</p>

`
   },

   {
      id: 7,
      part: 1,
      question: "अगर PDF पूरी तरह Image Based हो तो क्या RAG सीधे काम करेगा?",

      answer: `

<h3>उत्तर</h3>

<p>

नहीं।

</p>

<p>

पहले OCR करना होगा।

</p>

<pre>

Image

↓

OCR

↓

Text

↓

Chunk

↓

Embedding

↓

Vector DB

</pre>

<p>

OCR के बिना Embedding नहीं बनेगी।

</p>

<b>Interview Answer</b>

<p>

Image PDF के लिए पहले OCR जरूरी है।

</p>

`
   },

   {
      id: 8,
      part: 1,
      question: "अगर OCR ने OpenAI को 0penAl पढ़ लिया तो क्या होगा?",

      answer: `

<h3>उत्तर</h3>

<p>

गलत OCR

↓

गलत Text

↓

गलत Embedding

↓

Poor Retrieval

</p>

<p>

यानी OCR जितना अच्छा होगा

Retrieval भी उतनी अच्छी होगी।

</p>

<b>Interview Answer</b>

<p>

Garbage In, Garbage Out.

</p>

`
   },

   {
      id: 9,
      part: 1,
      question: "Document में Automobile लिखा है लेकिन User Car Search करता है। क्या Retrieval होगा?",

      answer: `

<h3>उत्तर</h3>

<p>

अधिकतर Cases में

हाँ।

</p>

<p>

Embedding Models शब्द नहीं,

उनका Meaning समझते हैं।

</p>

<pre>

Car

Vehicle

Automobile

</pre>

<p>

इनकी Semantic Similarity काफी अधिक होती है।

</p>

<b>Interview Answer</b>

<p>

Embedding आधारित Retrieval Meaning पर आधारित होती है।

</p>

`
   },

   {
      id: 10,
      part: 1,
      question: "अगर Elasticsearch से Search हो सकता है तो Vector Database की जरूरत क्यों है?",

      answer: `

<h3>उत्तर</h3>

<b>Keyword Search</b>

<p>

Car केवल Car ढूंढेगा।

</p>

<p>

Automobile नहीं मिलेगा।

</p>

<b>Vector Search</b>

<p>

Car

Vehicle

Automobile

इनके Meaning को समझ सकता है।

</p>

<p>

लेकिन

HTTP 404

Invoice-1001

PHP 8.4

जैसे Exact Keywords के लिए Keyword Search बेहतर रहती है।

</p>

<p>

इसलिए Production में Hybrid Search उपयोग होती है।

</p>

<b>Interview Answer</b>

<p>

Keyword Search Exact Match करती है जबकि Vector Search Meaning समझती है। Production Systems में Hybrid Search सबसे अच्छा विकल्प होती है।

</p>

`
   },
   {
id:11,
part:2,
question:"अगर RAG गलत Chunk Retrieve कर रहा है, तो आप Debugging कहाँ से शुरू करेंगे?",

answer:`

<h3>उत्तर</h3>

<p>सीधे किसी एक Component को दोष नहीं देना चाहिए।</p>

<p><b>Step 1</b></p>

<ul>
<li>Chunking सही हुई या नहीं?</li>
<li>क्या Sentence बीच में टूट गया?</li>
</ul>

<p><b>Step 2</b></p>

<ul>
<li>Embedding सही बनी?</li>
<li>OCR या Parsing में Error तो नहीं?</li>
</ul>

<p><b>Step 3</b></p>

<ul>
<li>Retriever Top-K में Relevant Chunk ला रहा है?</li>
</ul>

<p><b>Step 4</b></p>

<ul>
<li>अगर Retrieval सही है लेकिन Answer गलत है, तो समस्या Prompt या LLM में हो सकती है।</li>
</ul>

<b>Interview Answer</b>

<p>Production में Chunking → Embedding → Retriever → Prompt → LLM इस क्रम में Debug किया जाता है।</p>

`
},

{
id:12,
part:2,
question:"अगर 100 PDFs में से 60 लगभग एक जैसी हों, तो Retrieval में क्या समस्या आएगी?",

answer:`

<h3>उत्तर</h3>

<p>Retriever बार-बार एक जैसे Chunks वापस ला सकता है।</p>

<p>Example:</p>

<pre>
Top Results

PDF-1

PDF-3

PDF-8

PDF-11
</pre>

<p>सभी का Content लगभग समान हो सकता है।</p>

<b>Solution</b>

<ul>
<li>MMR Retrieval</li>
<li>Deduplication</li>
<li>Reranker</li>
</ul>

<b>Interview Answer</b>

<p>Duplicate Results Retrieval Diversity कम कर देते हैं।</p>

`
},

{
id:13,
part:2,
question:"अगर User केवल 'Leave' लिखता है, तो Retrieval कैसे Improve करेंगे?",

answer:`

<h3>उत्तर</h3>

<p>Query Expansion करेंगे।</p>

<pre>

Leave

↓

Annual Leave

↓

Paid Leave

↓

Leave Policy

↓

Employee Leave Rules

</pre>

<p>इससे Recall बढ़ जाती है।</p>

<b>Interview Answer</b>

<p>Short Queries को Expand करके बेहतर Retrieval प्राप्त किया जाता है।</p>

`
},

{
id:14,
part:2,
question:"User कहता है कि केवल HR Policy Document में Search करो। इसे कैसे करेंगे?",

answer:`

<h3>उत्तर</h3>

<p>Metadata Filtering का उपयोग करेंगे।</p>

<pre>

Department = HR

Year = 2025

Document = HR Policy.pdf

</pre>

<p>Retriever पहले Filter लगाएगा, फिर Search करेगा।</p>

<b>Interview Answer</b>

<p>Metadata Filtering Search Space कम करती है जिससे Speed और Accuracy दोनों बढ़ती हैं।</p>

`
},

{
id:15,
part:2,
question:"अगर एक Sentence दो Chunks में टूट जाए तो क्या समस्या होगी?",

answer:`

<h3>उत्तर</h3>

<p>Relevant Information अधूरी Retrieve हो सकती है।</p>

<pre>

Chunk 1

Python was developed

Chunk 2

by Guido Van Rossum

</pre>

<p>अगर केवल पहला Chunk मिला तो Answer अधूरा होगा।</p>

<b>Solution</b>

<ul>
<li>Overlap</li>
<li>Parent-Child Retrieval</li>
</ul>

<b>Interview Answer</b>

<p>Chunk Boundary पर Context टूटने से Retrieval खराब हो सकती है।</p>

`
},

{
id:16,
part:2,
question:"Retriever हमेशा Top-20 Results भेजता है। क्या यह सही Strategy है?",

answer:`

<h3>उत्तर</h3>

<p>ज़रूरी नहीं।</p>

<p>Problems:</p>

<ul>

<li>Noise बढ़ेगा</li>

<li>Latency बढ़ेगी</li>

<li>Context Window भर जाएगी</li>

<li>Cost बढ़ेगी</li>

</ul>

<p>Production में सामान्यतः Top-3, Top-5 या Top-8 का उपयोग किया जाता है।</p>

<b>Interview Answer</b>

<p>Optimal Top-K चुनना Retrieval Quality के लिए बहुत महत्वपूर्ण है।</p>

`
},

{
id:17,
part:2,
question:"अगर Top-20 सही नहीं है, तो हमेशा Top-1 क्यों नहीं?",

answer:`

<h3>उत्तर</h3>

<p>क्योंकि कई बार Answer एक से अधिक Chunks में होता है।</p>

<p>अगर केवल Top-1 भेजेंगे, तो Context अधूरा हो सकता है।</p>

<b>Interview Answer</b>

<p>Top-1 Precision बढ़ा सकता है लेकिन Recall कम कर देता है।</p>

`
},

{
id:18,
part:2,
question:"Hybrid Search कब उपयोग करनी चाहिए?",

answer:`

<h3>उत्तर</h3>

<p>जब Exact Keywords और Semantic Meaning दोनों महत्वपूर्ण हों।</p>

<b>Examples</b>

<ul>

<li>HTTP 404</li>

<li>Invoice-1001</li>

<li>PHP 8.4</li>

</ul>

<p>इनके लिए Keyword Search बेहतर है।</p>

<p>लेकिन Car और Automobile जैसे Meaning आधारित Search के लिए Semantic Search बेहतर है।</p>

<b>Interview Answer</b>

<p>Production Systems में Keyword + Semantic दोनों का संयोजन (Hybrid Search) सबसे अच्छा रहता है।</p>

`
},

{
id:19,
part:2,
question:"Chunk के साथ Page Number Store क्यों किया जाता है?",

answer:`

<h3>उत्तर</h3>

<p>Page Number Source Citation के लिए उपयोग किया जाता है।</p>

<p>Example:</p>

<pre>

Employee Handbook

Page 42

</pre>

<p>इसके अलावा Audit, Trust और Explainability के लिए भी उपयोगी है।</p>

<b>Interview Answer</b>

<p>Page Number Metadata Answer को Verify करने और Source दिखाने में मदद करता है।</p>

`
},

{
id:20,
part:2,
question:"अगर Embedding Model बदल दें, तो क्या पुराने Vectors उपयोग किए जा सकते हैं?",

answer:`

<h3>उत्तर</h3>

<p><b>नहीं।</b></p>

<p>हर Embedding Model अपना अलग Vector Space बनाता है।</p>

<p>इसलिए पुराने Vectors नए Model के साथ Compatible नहीं होते।</p>

<p>पूरे Documents को दोबारा Embed करके नया Index बनाना पड़ता है।</p>

<b>Interview Answer</b>

<p>Embedding Model बदलने पर Re-Embedding और Re-Indexing आवश्यक होती है।</p>

`
},
{
id:21,
part:3,
question:"अगर User का Answer तीन अलग-अलग Chunks में मौजूद हो तो क्या केवल Top-1 Chunk भेजना सही होगा?",

answer:`

<h3>उत्तर</h3>

<p>नहीं।</p>

<p>अगर जानकारी कई Chunks में फैली है, तो केवल Top-1 Chunk भेजने से उत्तर अधूरा हो सकता है।</p>

<p>ऐसे मामलों में Top-K Retrieval या Parent-Child Retrieval अधिक उपयोगी होता है।</p>

<b>Interview Answer</b>

<p>जब जानकारी कई Chunks में फैली हो, तो Multiple Relevant Chunks LLM को भेजने चाहिए।</p>

`
},

{
id:22,
part:3,
question:"अगर दो Chunks लगभग समान Score रखते हों, तो किसे चुनेंगे?",

answer:`

<h3>उत्तर</h3>

<p>केवल Similarity Score देखना पर्याप्त नहीं है।</p>

<p>Production Systems में अक्सर Reranker का उपयोग किया जाता है जो Query के Context के अनुसार बेहतर Chunk चुनता है।</p>

<b>Interview Answer</b>

<p>Final Selection के लिए Similarity Score के साथ Reranking का उपयोग किया जाता है।</p>

`
},

{
id:23,
part:3,
question:"Vector Search के बाद भी Reranker की आवश्यकता क्यों होती है?",

answer:`

<h3>उत्तर</h3>

<p>Vector Search तेज़ होता है लेकिन हमेशा सबसे Relevant Result पहले नहीं देता।</p>

<p>Reranker Top Retrieved Chunks को दोबारा Analyze करके उनकी Ranking सुधारता है।</p>

<b>Interview Answer</b>

<p>Vector Retrieval Recall बढ़ाता है, जबकि Reranker Precision बढ़ाता है।</p>

`
},

{
id:24,
part:3,
question:"अगर User केवल 'Python' लिखे, तो क्या पूरा Python Document Retrieve करना चाहिए?",

answer:`

<h3>उत्तर</h3>

<p>नहीं। Query बहुत Generic है।</p>

<p>System पहले Query Clarification या Query Expansion कर सकता है, जैसे:</p>

<ul>
<li>Python Basics</li>
<li>Python Functions</li>
<li>Python Classes</li>
<li>Python Decorators</li>
</ul>

<b>Interview Answer</b>

<p>Generic Queries के लिए Query Expansion या Clarification उपयोगी होती है।</p>

`
},

{
id:25,
part:3,
question:"अगर User गलत Spelling लिख दे, जैसे 'Pythn', तो क्या Retrieval Fail हो जाएगा?",

answer:`

<h3>उत्तर</h3>

<p>हमेशा नहीं।</p>

<p>Modern Embedding Models और Fuzzy Search कई बार ऐसी गलतियों को Handle कर लेते हैं।</p>

<p>लेकिन Exact Keyword Search में समस्या आ सकती है।</p>

<b>Interview Answer</b>

<p>Semantic Retrieval छोटे Typo को कई बार Handle कर सकता है, जबकि Keyword Search कम प्रभावी हो सकती है।</p>

`
},

{
id:26,
part:3,
question:"अगर Document हर दिन Update होता हो, तो Embeddings कैसे Manage करेंगे?",

answer:`

<h3>उत्तर</h3>

<p>पूरे Document को दोबारा Embed करना हमेशा आवश्यक नहीं होता।</p>

<p>केवल बदले हुए Chunks को Re-Embed करके Index Update किया जा सकता है।</p>

<b>Interview Answer</b>

<p>Incremental Indexing Production Systems में अधिक Efficient होती है।</p>

`
},

{
id:27,
part:3,
question:"अगर Retrieval सही है लेकिन LLM गलत Answer दे रहा है, तो समस्या कहाँ हो सकती है?",

answer:`

<h3>उत्तर</h3>

<ul>
<li>Prompt सही नहीं है।</li>
<li>Context बहुत बड़ा है।</li>
<li>LLM Hallucinate कर रहा है।</li>
<li>Instruction स्पष्ट नहीं है।</li>
</ul>

<b>Interview Answer</b>

<p>Correct Retrieval के बाद भी Prompt Design और Context Quality महत्वपूर्ण होती है।</p>

`
},

{
id:28,
part:3,
question:"अगर User एक ही प्रश्न बार-बार पूछता है, तो हर बार Retrieval करना चाहिए?",

answer:`

<h3>उत्तर</h3>

<p>ज़रूरी नहीं।</p>

<p>Frequently Asked Queries के लिए Cache का उपयोग किया जा सकता है।</p>

<p>इससे Latency और Cost दोनों कम हो जाती हैं।</p>

<b>Interview Answer</b>

<p>Repeated Queries के लिए Caching एक महत्वपूर्ण Optimization है।</p>

`
},

{
id:29,
part:3,
question:"अगर Document में Text के साथ Images भी हों, तो केवल Text Retrieval पर्याप्त होगा?",

answer:`

<h3>उत्तर</h3>

<p>हमेशा नहीं।</p>

<p>अगर महत्वपूर्ण जानकारी Images, Charts या Diagrams में है, तो Multimodal Retrieval की आवश्यकता होगी।</p>

<b>Interview Answer</b>

<p>Image आधारित जानकारी के लिए Multimodal RAG अधिक उपयुक्त होता है।</p>

`
},

{
id:30,
part:3,
question:"अगर User ऐसा प्रश्न पूछे जिसका उत्तर किसी भी Document में नहीं है, तो System को क्या करना चाहिए?",

answer:`

<h3>उत्तर</h3>

<p>System को स्पष्ट रूप से बताना चाहिए कि उपलब्ध Documents में इसका उत्तर नहीं मिला।</p>

<p>उसे अपनी Internal Knowledge से अनुमान लगाकर उत्तर नहीं देना चाहिए।</p>

<b>Interview Answer</b>

<p>Grounded RAG केवल Retrieved Context पर आधारित उत्तर देता है। यदि जानकारी उपलब्ध न हो, तो यह स्पष्ट रूप से बताना चाहिए।</p>

`
},
{
id:31,
part:4,
question:"User पूछता है: '2023 की Leave Policy और 2025 की Leave Policy में क्या अंतर है?' दोनों अलग-अलग Documents में हैं। क्या सामान्य RAG पर्याप्त होगा?",

answer:`

<h3>उत्तर</h3>

<p>सिर्फ एक Chunk Retrieve करना पर्याप्त नहीं होगा।</p>

<p>System को दोनों Documents से Relevant Chunks Retrieve करने होंगे।</p>

<pre>

2023 Policy
      ↓
Retrieve

2025 Policy
      ↓
Retrieve

      ↓

Compare

      ↓

Final Answer

</pre>

<p>LLM दोनों Policies की तुलना करके Difference बताएगा।</p>

<b>Interview Answer</b>

<p>Comparison वाले Questions में Multiple Relevant Documents Retrieve करके Comparative Reasoning करनी होती है।</p>

`
},

{
id:32,
part:4,
question:"Document में Leave Policy, Holiday Policy, Sick Leave और Maternity Leave हैं। User केवल 'Employee Leave Policy' पूछता है। क्या एक ही Query पर्याप्त है?",

answer:`

<h3>उत्तर</h3>

<p>हमेशा नहीं।</p>

<p>Production Systems अक्सर Query Expansion या Multi Query Retrieval का उपयोग करते हैं।</p>

<pre>

Employee Leave Policy

↓

Annual Leave

↓

Paid Leave

↓

Leave Rules

↓

Vacation Policy

</pre>

<p>फिर सभी Results Merge किए जाते हैं।</p>

<b>Interview Answer</b>

<p>Multi Query Retrieval अलग-अलग Queries बनाकर Recall बढ़ाती है।</p>

`
},

{
id:33,
part:4,
question:"तीन अलग-अलग Retrievers अलग-अलग Ranking दे रहे हैं। Final Result कैसे चुनेंगे?",

answer:`

<h3>उत्तर</h3>

<p>ऐसे मामलों में Reciprocal Rank Fusion (RRF) उपयोग किया जाता है।</p>

<p>यह सभी Retrievers की Ranking को Combine करके Final Ranking तैयार करता है।</p>

<p>इससे Single Retriever की Weakness कम हो जाती है।</p>

<b>Interview Answer</b>

<p>RRF कई Retrievers के Results को Ranking के आधार पर Merge करता है।</p>

`
},

{
id:34,
part:4,
question:"LLM का Context Window 128K Tokens है। क्या पूरा Document भेज देना चाहिए?",

answer:`

<h3>उत्तर</h3>

<p>नहीं।</p>

<p>बड़ा Context Window होने का मतलब यह नहीं कि पूरा Document भेज दिया जाए।</p>

<ul>

<li>Cost बढ़ेगी</li>

<li>Latency बढ़ेगी</li>

<li>Noise बढ़ेगा</li>

<li>Lost in the Middle Problem बढ़ सकती है</li>

</ul>

<b>Interview Answer</b>

<p>केवल Relevant Context ही LLM को भेजना चाहिए।</p>

`
},

{
id:35,
part:4,
question:"अगर उत्तर 10 अलग-अलग Chunks में फैला हो, तो क्या सभी Chunks LLM को भेज देंगे?",

answer:`

<h3>उत्तर</h3>

<p>हमेशा नहीं।</p>

<p>पहले Context Compression या Summarization किया जा सकता है।</p>

<pre>

10 Chunks

↓

Compress

↓

2-3 Relevant Chunks

↓

LLM

</pre>

<p>इससे Cost, Latency और Context Size कम होती है।</p>

<b>Interview Answer</b>

<p>Context Compression का उद्देश्य Relevant Information रखते हुए Context Size कम करना है।</p>

`
},

{
id:36,
part:4,
question:"Document में Employee → Manager → Department → Company जैसे Relationships हैं। क्या Normal RAG पर्याप्त होगा?",

answer:`

<h3>उत्तर</h3>

<p>Complex Relationship आधारित Queries में GraphRAG अधिक प्रभावी होता है।</p>

<pre>

Employee

↓

Manager

↓

Department

↓

Company

</pre>

<p>Graph Structure Relationships को Preserve करता है।</p>

<b>Interview Answer</b>

<p>Relationship आधारित Queries के लिए GraphRAG सामान्य Vector Search से बेहतर होता है।</p>

`
},

{
id:37,
part:4,
question:"User पूछता है: 'Raj किस Department में है?' फिर पूछता है: 'उस Department का Manager कौन है?' क्या हर बार नई Retrieval होगी?",

answer:`

<h3>उत्तर</h3>

<p>नहीं।</p>

<p>Conversational RAG Conversation History का उपयोग करता है।</p>

<p>'उस Department' का अर्थ पहले Answer से समझा जाएगा।</p>

<b>Interview Answer</b>

<p>Conversational RAG Follow-up Questions को Conversation Context के आधार पर समझता है।</p>

`
},

{
id:38,
part:4,
question:"कैसे पता चलेगा कि Retriever अच्छा काम कर रहा है?",

answer:`

<h3>उत्तर</h3>

<p>Retriever को Evaluation Metrics से Measure किया जाता है।</p>

<ul>

<li>Recall@K</li>

<li>Precision@K</li>

<li>MRR</li>

<li>NDCG</li>

<li>Hit Rate</li>

</ul>

<p>अगर Relevant Chunk Top Results में आ रहा है, तो Retrieval अच्छा माना जाएगा।</p>

<b>Interview Answer</b>

<p>Retriever की Quality को Retrieval Metrics से Evaluate किया जाता है।</p>

`
},

{
id:39,
part:4,
question:"LLM ने सही Answer दिया लेकिन गलत Source दिखा दिया। क्या यह Production में Problem है?",

answer:`

<h3>उत्तर</h3>

<p>हाँ।</p>

<p>Enterprise Systems में Answer के साथ सही Citation भी आवश्यक है।</p>

<p>गलत Citation से User का Trust कम हो सकता है।</p>

<b>Interview Answer</b>

<p>Production RAG में Correct Answer के साथ Correct Citation भी आवश्यक है।</p>

`
},

{
id:40,
part:4,
question:"User पूछता है: 'Company के CEO की Salary कितनी है?' लेकिन Documents में इसका उत्तर नहीं है। LLM को Internet से जानकारी पता है। अब क्या करना चाहिए?",

answer:`

<h3>उत्तर</h3>

<p>अगर यह Document Grounded RAG है, तो LLM को केवल Retrieved Context पर आधारित उत्तर देना चाहिए।</p>

<pre>

मुझे उपलब्ध Documents में
इस प्रश्न का उत्तर नहीं मिला।

</pre>

<p>Model को अपनी Internal Knowledge से उत्तर नहीं बनाना चाहिए।</p>

<b>Interview Answer</b>

<p>Grounded RAG केवल Retrieved Context पर आधारित उत्तर देता है। जानकारी उपलब्ध न होने पर स्पष्ट रूप से यह बताना चाहिए।</p>

`
},
{
id:41,
part:5,
question:"Retriever ने गलत Chunks Retrieve कर दिए। अब System को क्या करना चाहिए?",

answer:`

<h3>उत्तर</h3>

<p>Production System में सीधे LLM को Answer Generate नहीं करने देना चाहिए।</p>

<p>पहले Retrieval Quality Check करनी चाहिए।</p>

<pre>

User Query

↓

Retrieve

↓

Quality Check

↓

Poor Retrieval ?

↓

Yes

↓

Retrieve Again

↓

LLM

</pre>

<p>इसे Corrective RAG (CRAG) Approach कहा जाता है।</p>

<b>Interview Answer</b>

<p>यदि Retrieved Context पर्याप्त या Relevant नहीं है, तो System को दोबारा Retrieval करना चाहिए।</p>

`
},

{
id:42,
part:5,
question:"अगर User बहुत Complex Question पूछे, तो क्या एक ही Retrieval पर्याप्त होगी?",

answer:`

<h3>उत्तर</h3>

<p>हमेशा नहीं।</p>

<p>Complex Queries को छोटे-छोटे Tasks में Divide किया जा सकता है।</p>

<pre>

Main Question

↓

Sub Question 1

↓

Sub Question 2

↓

Comparison

↓

Final Answer

</pre>

<p>इसे Agentic RAG Approach कहा जाता है।</p>

<b>Interview Answer</b>

<p>Complex Problems को Multiple Retrieval Steps में Solve करना अधिक प्रभावी होता है।</p>

`
},

{
id:43,
part:5,
question:"अगर LLM को लगे कि उपलब्ध Context पर्याप्त नहीं है, तो क्या करना चाहिए?",

answer:`

<h3>उत्तर</h3>

<p>System को आवश्यकता होने पर दोबारा Retrieval करनी चाहिए।</p>

<pre>

Retrieve

↓

Generate Answer

↓

Self Evaluation

↓

Need More Context?

↓

Yes

↓

Retrieve Again

</pre>

<p>इसे Self-RAG Approach कहा जाता है।</p>

<b>Interview Answer</b>

<p>Self-RAG आवश्यकता पड़ने पर अतिरिक्त Context Retrieve कर सकता है।</p>

`
},

{
id:44,
part:5,
question:"अगर आपके पास 1 करोड़ Documents हों, तो क्या सभी पर Vector Search करेंगे?",

answer:`

<h3>उत्तर</h3>

<p>नहीं।</p>

<p>पहले Metadata Filtering करके Search Space कम किया जाता है।</p>

<pre>

Country = India

↓

Department = HR

↓

Year = 2025

↓

Vector Search

</pre>

<p>इससे Retrieval तेज़ और अधिक Accurate हो जाती है।</p>

<b>Interview Answer</b>

<p>Large Scale Systems में पहले Metadata Filtering, फिर Vector Retrieval किया जाता है।</p>

`
},

{
id:45,
part:5,
question:"Embedding Model पुराना हो गया है और Domain बदल चुका है। इसका क्या प्रभाव पड़ेगा?",

answer:`

<h3>उत्तर</h3>

<p>पुराना Embedding Model नई Terminology को सही तरह Represent नहीं कर पाएगा।</p>

<p>इससे Semantic Similarity और Retrieval Quality दोनों प्रभावित हो सकती हैं।</p>

<p>ऐसे मामलों में Re-Embedding करना उचित होता है।</p>

<b>Interview Answer</b>

<p>Embedding Drift के कारण समय के साथ Retrieval Quality कम हो सकती है।</p>

`
},

{
id:46,
part:5,
question:"FAISS, Pinecone, Qdrant और Milvus में से कैसे चुनेंगे?",

answer:`

<h3>उत्तर</h3>

<ul>

<li><b>FAISS</b> - Local, Fast, Open Source</li>

<li><b>Pinecone</b> - Managed Cloud Service</li>

<li><b>Qdrant</b> - Excellent Metadata Filtering</li>

<li><b>Milvus</b> - Enterprise Scale Deployments</li>

</ul>

<p>Selection Scale, Budget, Infrastructure और Operational Requirements पर निर्भर करता है।</p>

<b>Interview Answer</b>

<p>Vector Database का चयन Use Case और Deployment Requirements के आधार पर किया जाता है।</p>

`
},

{
id:47,
part:5,
question:"Million Vectors होने पर Exact Search क्यों नहीं करते?",

answer:`

<h3>उत्तर</h3>

<p>Exact Search बहुत Slow हो जाती है।</p>

<p>इसलिए ANN (Approximate Nearest Neighbor) Algorithms का उपयोग किया जाता है।</p>

<ul>

<li>HNSW</li>

<li>IVF</li>

<li>PQ</li>

</ul>

<p>इनसे Speed और Scalability दोनों बेहतर होती हैं।</p>

<b>Interview Answer</b>

<p>Large Scale Retrieval के लिए ANN Algorithms उपयोग किए जाते हैं।</p>

`
},

{
id:48,
part:5,
question:"500 Pages के Document में केवल Decorators की जानकारी चाहिए। क्या पूरा Document Retrieve करेंगे?",

answer:`

<h3>उत्तर</h3>

<p>नहीं।</p>

<p>Hierarchical Retrieval या RAPTOR जैसी Techniques उपयोग की जा सकती हैं।</p>

<pre>

Python

↓

Functions

↓

Classes

↓

Decorators

</pre>

<p>केवल Relevant Branch Retrieve होगी।</p>

<b>Interview Answer</b>

<p>Hierarchical Retrieval केवल आवश्यक हिस्से को Retrieve करता है।</p>

`
},

{
id:49,
part:5,
question:"User 'Readonly Property' पूछता है लेकिन बार-बार 'Readonly Class' Retrieve हो रही है। क्यों?",

answer:`

<h3>उत्तर</h3>

<p>दोनों Terms Semantic रूप से काफी Similar हो सकती हैं।</p>

<p>Embedding Model उन्हें समान Meaning वाला मान सकता है।</p>

<p>Solution:</p>

<ul>

<li>Hybrid Search</li>

<li>Better Reranker</li>

<li>Metadata Filtering</li>

<li>Query Rewriting</li>

</ul>

<b>Interview Answer</b>

<p>Semantic Similarity के कारण Confusion हो सकती है, जिसे Hybrid Search और Reranking से कम किया जा सकता है।</p>

`
},

{
id:50,
part:5,
question:"अगर आपको Zero से Production RAG System Design करना हो, तो High-Level Architecture क्या होगा?",

answer:`

<h3>उत्तर</h3>

<pre>

User Query

↓

Query Processing

↓

Metadata Filtering

↓

Hybrid Retrieval

↓

Top-K Retrieval

↓

Reranker

↓

Context Compression

↓

Prompt Builder

↓

LLM

↓

Grounded Answer

↓

Citation

↓

Monitoring

</pre>

<p>Production Systems में Monitoring भी आवश्यक होती है।</p>

<ul>

<li>Latency</li>

<li>Recall</li>

<li>Cost</li>

<li>Hallucination Rate</li>

<li>User Feedback</li>

</ul>

<b>Interview Answer</b>

<p>Production RAG केवल Retrieval नहीं है, बल्कि Query Processing, Retrieval, Reranking, Context Optimization, LLM, Citation, Monitoring और Continuous Evaluation का पूरा Pipeline है।</p>

`
}

];