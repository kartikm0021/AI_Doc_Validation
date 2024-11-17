Requirements for Rules and Ruleset Modules


This document provides a full picture of the Rules Module and Ruleset Module, incorporating features for creation, listing, dependencies, tagging, categorization, and management workflows. The requirements also include the integration of categories for better organization and scalability.

1. Rules Module
1.1 Objective
The Rules Module allows users to:

Create, edit, test, and delete validation rules for multi-modal media types.
Understand and manage rule dependencies with rulesets and complex rules.
Organize rules with tags and categories for improved management and usability.
View and analyze rule usage across the system.
1.2 Features
1.2.1 Rule Types
Standalone Rules:

Independent validation logic for specific media types.
Example: "Flag prohibited phrases in text."
Complex Rules:

Combine multiple rules (standalone or sub-rules) using logical operators (AND, OR, NOT).
Example: (Prohibited Phrases AND Missing Disclaimer) OR Brand Logo Detection.
Sub-Rules:

Reusable, modular rules included in standalone or complex rules.
Example: "Detect prohibited phrases in captions."
1.2.2 Multi-Modal Media Support
Rules should support validation for:

Text: Analyze entire documents or specific sections (e.g., headers, footers).
Video: Validate captions, specific time ranges, or metadata.
Audio: Transcribe and analyze speech for specific terms.
Images: OCR-based text analysis or visual detection (e.g., logos).
1.2.3 Rule Management
Create Rule:
Define name, description, tags, categories, media type(s), and validation logic.
Edit Rule:
Modify rule details or logic, with warnings for dependencies.
Delete Rule:
Remove a rule with visibility into where it is used (rulesets, complex rules).
Test Rule:
Upload sample media and validate the rule against it.
View Rule Details:
Display metadata, media types, validation logic, dependencies, tags, and categories.
1.2.4 Rule Dependencies
View Dependencies:
List all rulesets and complex rules that use a given rule.
Warnings for Dependencies:
Notify users when editing or deleting a rule that affects dependent entities.
Graphical View:
Optionally provide a visual representation of dependencies between rules, rulesets, and complex rules.
1.2.5 Tagging and Categorization
Tagging:
Flexible, user-defined labels for rules.
Example Tags: "Marketing," "Compliance," "Legal."
Categorization:
Rigid, hierarchical groupings for structured navigation.
Example Categories:
Marketing → Product Brochures
Compliance → Regulatory Guidelines
1.2.6 Rule Listing and Filtering
Search and Filter:
Search by name or tags.
Filter by:
Rule Type: Standalone, Complex, Sub-Rule.
Media Type: Text, Video, Audio, Image.
Categories: Predefined hierarchical categories.
List View:
Display rule name, type, media type, tags, categories, and usage status (e.g., active/inactive).
1.3 Wireframes
1.3.1 Rules Dashboard
sql
Copy code
+-----------------------------------------------+
| Rules Module                                  |
+-----------------------------------------------+
| [ Create New Rule ]                           |
|                                               |
| Search: [Input Field: Search by name or tag]  |
| Filter By:                                    |
| - Rule Type: [✓ Standalone] [✓ Sub-Rule]      |
| - Media Type: [✓ Text] [✓ Video]              |
| - Categories: [Dropdown: Marketing → Ads]     |
|                                               |
| Rules List:                                   |
| +-------------------------------------------+ |
| | Rule Name         | Categories           | |
| +-------------------------------------------+ |
| | Prohibited Phrases| Marketing → Ads      | |
| | Missing Disclaimer| Compliance → Disclaimers|
| +-------------------------------------------+ |
+-----------------------------------------------+
1.3.2 Rule Details with Dependencies
yaml
Copy code
+-----------------------------------------------+
| Rule Details: Prohibited Phrases              |
+-----------------------------------------------+
| Name: Prohibited Phrases                      |
| Type: Sub-Rule                                |
| Media Types: Text, Video                      |
| Tags: Marketing, Compliance                   |
| Categories: Marketing → Ads, Compliance → Disclaimers |
|                                               |
| Validation Logic:                             |
| - Text: "Flag phrases like 'guaranteed...'"   |
| - Video: "Check captions for 'risk-free.'"    |
|                                               |
| Dependencies:                                 |
| - Used in Rulesets:                           |
|   1. Marketing Content                        |
|   2. Compliance                               |
|                                               |
| - Used in Complex Rules:                      |
|   1. Marketing Validation                     |
|                                               |
| Actions:                                      |
| - [ Edit Rule ] [ Delete Rule ]               |
+-----------------------------------------------+
1.4 APIs for Rules
List Rules: GET /api/rules
Create Rule: POST /api/rules
Edit Rule: PUT /api/rules/{rule_id}
Delete Rule: DELETE /api/rules/{rule_id}
Test Rule: POST /api/rules/{rule_id}/test
Get Rule Dependencies: GET /api/rules/{rule_id}/dependencies
Assign Categories: PUT /api/rules/{rule_id}/categories
2. Ruleset Module
2.1 Objective
The Ruleset Module groups rules into reusable sets for batch validation and categorizes them for easy navigation.

2.2 Features
Ruleset Management
Create Ruleset:
Define name, description, tags, and categories.
Add rules from the repository.
Edit Ruleset:
Add or remove rules, update tags, categories, and descriptions.
Delete Ruleset:
Remove rulesets with warnings for active usage.
View Ruleset Details:
List associated rules, tags, categories, and application logic.
Adding/Deleting Rules in Rulesets
Add Rules:
Search and filter the rule repository to add multiple rules.
Delete Rules:
Remove rules with dependency checks for complex rules.
Ruleset Application
Apply Ruleset:
Upload media and apply all associated rules.
Unified Results:
Consolidate results for all rules in the ruleset.
Categorization in Rulesets
Assign one or more categories to a ruleset.
Filter and browse rulesets by categories.
2.3 Wireframes
2.3.1 Ruleset Creation
sql
Copy code
+-----------------------------------------------+
| Create New Ruleset                            |
+-----------------------------------------------+
| Step 1: Define Ruleset Details                |
| - Name: [Marketing Content Validation]        |
| - Description: [Validates marketing brochures...]|
| Tags: [Marketing, Multi-Modal]                |
| Categories:                                   |
| [ Dropdown: Select or Create Category ]       |
| - Selected: Marketing → Product Brochures     |
|                                               |
| Step 2: Add Rules                             |
| +-------------------------------------------+ |
| | Rule Name            | Type     | Add     | |
| +-------------------------------------------+ |
| | Prohibited Phrases   | Sub-Rule | [ Add ] | |
| | Missing Disclaimer   | Standalone| [ Add ]| |
| +-------------------------------------------+ |
|                                               |
| [ Save Ruleset ]                              |
+-----------------------------------------------+
2.4 APIs for Rulesets
List Rulesets: GET /api/rulesets
Create Ruleset: POST /api/rulesets
Edit Ruleset: PUT /api/rulesets/{ruleset_id}
Add Rules to Ruleset: POST /api/rulesets/{ruleset_id}/add-rules
Delete Rules from Ruleset: POST /api/rulesets/{ruleset_id}/remove-rules
Apply Ruleset: POST /api/rulesets/{ruleset_id}/apply
Assign Categories: PUT /api/rulesets/{ruleset_id}/categories
3. Benefits of Adding Categories
Improved Organization:
Logical grouping simplifies navigation and management.
Enhanced Search and Filtering:
Users can quickly find rules or rulesets based on their categories.
Scalability:
Supports growth of the rule repository without becoming unmanageable.
Efficient Management:
Admins can manage categories to reflect organizational needs.