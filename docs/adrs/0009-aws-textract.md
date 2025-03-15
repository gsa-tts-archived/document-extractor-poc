# 9. Use AWS Textract for OCR

Date: 2025-03-14

## Status

Accepted.

## Context

A big part of our application is extracting text from uploaded documents.  This means Optical Character Recognition
(OCR).  There are many solutions to OCR.

Some that we explored are...
1. AWS Textract.
2. Tesseract.
3. EasyOCR.
4. Paddle OCR.

Textract supports many different types of extraction: (standard text, forms, tables, queries, etc.), can be trained for
better results, and can guess the keys of the fields in a form.  In a trial test, Textract significantly out-performed
Tesseract at extracting structured data.  Given Tesseract's limitations, we decided not to test other open-source tools,
as Textract was already delivering strong results.

Some OCR solutions have deep learning models, which can improve OCR accuracy for complex documents and handwriting.
Others may allow us to bring our own models, but both of these options would require additional and extensive up-front
work to get the capabilities to match Textract.

Textract comes with a price per use which can be costly for a high volume of usage, compared to open-source options that
do not have a price per use.  Open-source options, on the other hand, have less out-of-the box controls, resulting in
more developer time spent up-front in building up capabilities and a higher cost of maintenance, for example, with
increased costs for memory and CPU time.

## Decision

Given our focus on demonstrating what an AI-powered-OCR with self-learning capabilities can do for document processing staff we have elected, in the short term, to keep using AWS Textract.

Open-source OCR may be more cost-effective in the long run, but it requires significant initial investment that we’d
like to avoid, given the limited scope of our proof-of-concept.  We will continue to weigh trade-offs as we gain a
clearer runway of a fully operational product.

## Consequences

To support the ability to pivot in the future, we will utilize an "interface" so we don't need to change code everywhere
when we choose to adopt a different solution.
