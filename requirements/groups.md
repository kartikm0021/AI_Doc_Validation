# Supporting Multiple Groups per AD Group

If you need to map 2 or more logical groups to a single Active Directory (AD) group, the platform can incorporate sub-groups or logical groupings within the AD group. This design provides flexibility for organizations where a single AD group encompasses multiple logical divisions or roles.

## Conceptual Approach

### Sub-Groups:

Create sub-groups under a parent AD group to divide users logically within the same AD group.
Example:
    AD Group: Marketing
        Sub-Group 1: Marketing → Content
        Sub-Group 2: Marketing → Analytics

### Roles within Groups:

Users in the AD group are assigned roles or tags that determine their logical grouping.
Example:
    AD Group: Compliance
        User A: Compliance → Regulatory
        User B: Compliance → Legal

### Mapping Users Dynamically:

Use metadata or attributes from the AD group (e.g., job title, department) to dynamically map users to logical groups.


## Key Features

### 1. Logical Grouping within AD Groups

    Each AD group can have multiple logical groups (e.g., sub-groups or divisions).
    Logical groups are maintained in the platform, not directly in AD.
    Rules and rulesets are associated with these logical groups.
### 2. Flexible Group Assignment

    Users are mapped to one or more logical groups during login or setup.
    Admins can assign users to specific logical groups manually or dynamically based on AD attributes.

### 3. Cross-Logical Group Sharing

    Allow sharing of rules and rulesets between logical groups under the same or different AD groups.


# Updated Group Management Features

### 1. Logical Group Creation

    Admins create logical groups within a parent AD group.
    Logical groups are independent but share the parent AD group for user authentication.

### Wireframe: Logical Group Creation
+-----------------------------------------------+
| Create Logical Group                          |
+-----------------------------------------------+
| Parent AD Group: [ Dropdown: Marketing ]      |
| Logical Group Name: [ Input Field ]           |
| Description: [ Optional Description ]         |
|                                               |
| [ Cancel ]  [ Create Logical Group ]          |
+-----------------------------------------------+

### 2. User Assignment to Logical Groups

    Assign users to logical groups dynamically based on AD attributes or manually via the admin interface.

Example:
    AD Group: Compliance
        Logical Group 1: Regulatory (Users: A, B)
        Logical Group 2: Legal (Users: C, D)

### Wireframe: User Assignment

+-----------------------------------------------+
| Assign Users to Logical Group                 |
+-----------------------------------------------+
| Logical Group: [ Dropdown: Compliance → Legal ]|
|                                               |
| Available Users (AD Group: Compliance):       |
| +-------------------------------------------+ |
| | User Name       | Email           | Add   | |
| +-------------------------------------------+ |
| | John Doe        | john@company.com| [ Add ]|
| | Jane Smith      | jane@company.com| [ Add ]|
| +-------------------------------------------+ |
|                                               |
| [ Cancel ]  [ Assign Users ]                  |
+-----------------------------------------------+

### 3. Logical Group Association for Rules and Rulesets

    Rules and rulesets can be assigned to one or more logical groups.
    Cross-group sharing is supported.

### Wireframe: Rule Creation with Multiple Group Assignment
+-----------------------------------------------+
| Create New Rule                               |
+-----------------------------------------------+
| Rule Name: [ Input Field: Prohibited Phrases ]|
| Assigned Groups:                              |
| [✓] Marketing → Content                      |
| [✓] Marketing → Analytics                    |
|                                               |
| Description: [ Optional Description ]         |
|                                               |
| [ Save Rule ]                                 |
+-----------------------------------------------+


### Improved Logical Group ID Design

#### Objective

The Logical Group ID should:

Be unique across all logical groups.
Be human-readable to aid debugging and management.
Follow a predictable and hierarchical structure that relates to the parent AD group.


#### Proposed Format

    Parent AD Group Name → Logical Group Name
    Example: Marketing → Content
<parent_ad_group_id>_<logical_group_name_slug>


#### Parent AD Group ID:

    This ensures that the logical group is tied to its AD group.
    Example: ad_group_marketing.

#### Logical Group Name Slug:

    Convert the logical group name into a lowercase, slugified format.
    Replace spaces and special characters with underscores for consistency.
    Example: "Content Team" → content_team.

#### Final Logical Group ID:

    Combine the two components using an underscore.
    Example: ad_group_marketing_content_team.



### Key Features of This Format
- Human-Readable:
    Clear association between a logical group and its parent AD group.
- Uniqueness:
    Uniqueness is ensured by combining the parent AD group and logical group name.
- Predictability:
    Easy to derive or reverse-engineer the logical group ID from its name and parent AD group.

#### Logical Group ID Creation Workflow

1. Input
    Parent AD Group ID: ad_group_marketing
    Logical Group Name: Content Team
2. Generate the Slug
    Convert the logical group name into a slug: content_team.
3. Combine with Parent AD Group ID
    Combine ad_group_marketing and content_team:
        Logical Group ID: ad_group_marketing_content_team.
4. Example IDs
    Parent AD Group ID	Logical Group Name	Logical Group ID
    ad_group_marketing	Content Team	ad_group_marketing_content_team
    ad_group_marketing	Analytics	ad_group_marketing_analytics
    ad_group_compliance	Regulatory	ad_group_compliance_regulatory


### Updated API for Logical Group Creation

#### API Endpoint

    Endpoint: POST /api/groups/logical

#### Payload:
{
  "parent_ad_group_id": "ad_group_marketing",
  "logical_group_name": "Content Team",
  "description": "Team responsible for marketing content"
}


#### Backend Processing

    Parse the parent_ad_group_id and logical_group_name.
    Generate the Logical Group ID using the slugified name.
    Store the Logical Group ID and associated details in the database.

#### Response

{
  "status": "success",
  "logical_group_id": "ad_group_marketing_content_team"
}


### Handling Duplicates

#### Duplicate Logical Group Names:

    If a logical group with the same name exists under the same parent AD group, reject the request with an error.

Example Error:
{
  "status": "error",
  "message": "A logical group with the name 'Content Team' already exists for AD group 'ad_group_marketing'."
}

#### Duplicate Logical Group IDs Across AD Groups:

    Logical group IDs are unique due to their combination of the parent AD group ID and slug, ensuring no conflicts across different AD groups.

#### Group Management Example

##### Create Logical Groups

    Input:

{
  "parent_ad_group_id": "ad_group_marketing",
  "logical_group_name": "Analytics",
  "description": "Team responsible for marketing analytics"
}

    Generated Logical Group ID: ad_group_marketing_analytics

##### List Logical Groups

    API: GET /api/groups/logical
Response:
{
  "logical_groups": [
    {
      "id": "ad_group_marketing_content_team",
      "name": "Content Team",
      "parent_ad_group_id": "ad_group_marketing",
      "description": "Team responsible for marketing content"
    },
    {
      "id": "ad_group_marketing_analytics",
      "name": "Analytics",
      "parent_ad_group_id": "ad_group_marketing",
      "description": "Team responsible for marketing analytics"
    }
  ]
}

#### Advantages of This Approach

- Hierarchical and Structured:
    The logical group ID explicitly ties the group to its parent AD group.
- Uniqueness and Predictability:
    Logical group IDs are unique across the system and follow a predictable format.
- Scalability:
    Supports large-scale setups with multiple logical groups under various AD groups.
- Human-Readable and Debug-Friendly:
    The ID format is easy to interpret and manage for administrators.



### Slugification Rules and Error Handling for Logical Group IDs

Slugification ensures that logical group names are converted into a standardized, URL-safe, and unique format for use in Logical Group IDs. Below are detailed rules, examples, and error-handling mechanisms to cover edge cases.

#### Slugification Rules

1.1 Basic Rules

    Convert to Lowercase:

    All letters are converted to lowercase for consistency.
    Example: Content Team → content team.

    Replace Spaces with Underscores:

    Spaces are replaced with underscores to ensure the slug is a single continuous string.
    Example: Content Team → content_team.

    Remove Special Characters:

    Characters that are not alphanumeric or underscores are removed.
    Example: Content & Analytics! → content_analytics.

    Trim Leading and Trailing Underscores:

    Any extra underscores at the start or end are removed.
    Example: _content_team_ → content_team.

1.2 Advanced Rules

    Handle Consecutive Spaces or Special Characters:

    Replace consecutive spaces or special characters with a single underscore.
    Example: Content Team!!! → content_team.

    Replace Non-ASCII Characters:

    Convert non-ASCII characters to their closest ASCII equivalent (if possible).
    Example: Crème Brûlée → creme_brulee.

    Remove Duplicate Slugs:

    If two logical groups under the same parent AD group result in the same slug, append a numeric suffix to differentiate.

Example:
    Content Team → content_team
    Content Team (second group) → content_team_1.

#### Error Handling

##### Duplicate Logical Group Names

    Scenario: Two logical groups with identical names are created under the same parent AD group.
    Resolution:
        Check the database for existing slugs under the same parent AD group.
        If a duplicate slug is found, append a numeric suffix to create a unique slug.

Example:
    Logical Group Name: Content Team
    Generated Slug: content_team
    Logical Group Name: Content Team (second entry under the same parent)
    Generated Slug: content_team_1

##### Duplicate Logical Group Names Across Different Parent AD Groups

    Logical group IDs are unique because they include the parent AD group ID.
    No error occurs if two logical groups with the same name exist under different parent AD groups.

Example:
    Parent AD Group: ad_group_marketing
    Logical Group Name: Content Team
    Logical Group ID: ad_group_marketing_content_team

    Parent AD Group: ad_group_compliance
    Logical Group Name: Content Team
    Logical Group ID: ad_group_compliance_content_team

##### Special Characters and Encoding Issues

    Special characters should be removed or replaced during slug generation to ensure a URL-safe string.

##### Error Handling:

    If an invalid character is detected during input validation, prompt the user to modify the name.

Example:
    Input: Content Team @ HQ!
    Warning: "Group names cannot include special characters like '@' or '!'. Please revise."

#### Slugification Examples

Input Variations and Output Slugs
    Parent AD Group	Logical Group Name	Generated Slug	Logical Group ID
    ad_group_marketing	Content Team	content_team	ad_group_marketing_content_team
    ad_group_marketing	Content Team (duplicate)	content_team_1	ad_group_marketing_content_team_1
    ad_group_marketing	Analytics	analytics	ad_group_marketing_analytics
    ad_group_compliance	Content Team	content_team	ad_group_compliance_content_team
    ad_group_compliance	Regulatory Affairs	regulatory_affairs	ad_group_compliance_regulatory_affairs
    ad_group_marketing	Content & Analytics!	content_analytics	ad_group_marketing_content_analytics
    ad_group_marketing	Crème Brûlée	creme_brulee	ad_group_marketing_creme_brulee
    ad_group_compliance	_Risk Management_	risk_management	ad_group_compliance_risk_management

#### API Example with Slugification

##### Logical Group Creation API

    Endpoint: POST /api/groups/logical

Payload:

{
  "parent_ad_group_id": "ad_group_marketing",
  "logical_group_name": "Content & Analytics!",
  "description": "Marketing content and analytics team"
}

Backend Processing:

    Generate slug: content_analytics
    Create Logical Group ID: ad_group_marketing_content_analytics

Response:

{
  "status": "success",
  "logical_group_id": "ad_group_marketing_content_analytics",
  "slug": "content_analytics"
}

##### Error Response for Duplicate Logical Groups

    Request:

{
  "parent_ad_group_id": "ad_group_marketing",
  "logical_group_name": "Content Team"
}

Backend Processing:

    Check database: ad_group_marketing_content_team exists.
    Generate unique slug: content_team_1.

Error Response (if uniqueness isn’t automatically resolved):

{
  "status": "error",
  "message": "A logical group with the name 'Content Team' already exists for AD group 'ad_group_marketing'. Try a different name."
}

#### Benefits of These Rules

- Consistency:
    All logical group IDs follow a standard, predictable format.
- Uniqueness:
    Ensures that logical group IDs are unique across the platform.
- Human-Readable:
    Logical group IDs are easy to interpret and debug.
- Error Prevention:
    Prevents collisions and provides clear guidance for duplicate or invalid input.



### User Management Screens for Maintaining Users in Logical Groups

This section outlines the requirements, workflows, and designs for user management screens to manage users in logical groups. Since users log in with their LAN IDs or AD email IDs, the system integrates seamlessly with Active Directory to fetch user details and manage group memberships.

#### Key Features
1.1 Adding Users to Logical Groups
Admins can add users to logical groups by searching for their LAN ID or AD email ID.
    User details are fetched automatically from AD.
    Support for batch addition of users (via CSV upload or bulk selection).

1.2 Removing Users from Logical Groups
    Admins can remove users from logical groups.
    Show a confirmation dialog to ensure intentional removal.

#### Viewing Users in Logical Groups

    Display a list of users assigned to a logical group, including:
    - Full Name
    - LAN ID
    - AD Email
    - Role within the group (Owner, Editor, Viewer).

#### Roles within Logical Groups

    Roles:
    - Owner: Full control over rules and rulesets.
    - Editor: Can edit rules and rulesets but cannot manage users.
    - Viewer: Can only view rules and rulesets.

Admins can assign or update roles for users within a logical group.

#### User Synchronization with AD

    The system syncs periodically with AD to fetch:
    - User details for new LAN IDs or email IDs.
    - Updated group memberships.

#### Workflow for Managing Users
2.1 Adding Users to Logical Groups
    - Admin navigates to the Group Management Dashboard.
    - Selects a logical group and opens the Add Users screen.
    - Searches for users by LAN ID or AD email ID.
    - Adds users to the group with an assigned role.

2.2 Removing Users
    - Admin navigates to the list of users in a logical group.
    - Selects one or more users for removal.
    - Confirms the removal action.

2.3 Assigning or Changing Roles
    - Admin selects a user from the user list.
    - Updates the user's role within the logical group.
    
#### User Screens
3.1 Logical Group User Management Screen

+-----------------------------------------------+
+-----------------------------------------------+
| Manage Users: Marketing → Content Team        |
+-----------------------------------------------+
| Add New User: [ Input: Search by LAN ID/Email ]|
|                                               |
| User List:                                    |
| +-------------------------------------------+ |
| | Full Name   | LAN ID    | Role   | Actions | |
| +-------------------------------------------+ |
| | John Doe    | john123   | Owner  | [ Edit ] [ Remove ] |
| | Jane Smith  | jane456   | Viewer | [ Edit ] [ Remove ] |
| +-------------------------------------------+ |
|                                               |
| Batch Actions:                                |
| [ Select All ]  [ Remove Selected ]           |
+-----------------------------------------------+

3.2 Add Users to Logical Group

+-----------------------------------------------+
| Add Users: Marketing → Content Team           |
+-----------------------------------------------+
| Search User: [ Input: Search by LAN ID/Email ]|
| +-------------------------------------------+ |
| | Full Name   | LAN ID    | Email       | Add | |
| +-------------------------------------------+ |
| | John Doe    | john123   | john@company.com | [ Add ] |
| | Jane Smith  | jane456   | jane@company.com | [ Add ] |
| +-------------------------------------------+ |
|                                               |
| Batch Upload: [ Upload CSV File ]             |
|                                               |
| [ Cancel ]  [ Add Selected Users ]            |
+-----------------------------------------------+
3.3 Role Assignment

+-----------------------------------------------+
| Assign Role: John Doe                         |
+-----------------------------------------------+
| Logical Group: Marketing → Content Team       |
|                                               |
| Current Role: [ Dropdown: Owner ]             |
| [✓] Owner                                     |
| [ ] Editor                                    |
| [ ] Viewer                                    |
|                                               |
| [ Cancel ]  [ Save Changes ]                  |
+-----------------------------------------------+
#### Validation and Error Handling

4.1 Adding Invalid Users

    Scenario: Admin enters a LAN ID or email ID that does not exist in AD.
    Resolution:
        Show an error message and log the failed attempt.
Example:
    Error: The LAN ID 'invalid123' does not exist in Active Directory. Please check the input or contact IT support.

4.2 Duplicate User Assignment

    Scenario: Admin tries to add a user who is already in the logical group.
    Resolution:
        Display a warning but do not re-add the user.

Example:
    Warning: The user 'john123' is already a member of the group.

4.3 Role Conflicts

    Scenario: Admin tries to downgrade the role of the only Owner in the group.
    Resolution:
        Prevent the action and display a message.
Example:
    Error: You cannot remove the 'Owner' role from the only owner in the group. Assign a new owner before proceeding.

#### APIs for User Management

5.1 List Users in a Logical Group

    Endpoint: GET /api/groups/{logical_group_id}/users
Response:
{
  "users": [
    {
      "lan_id": "john123",
      "email": "john@company.com",
      "name": "John Doe",
      "role": "Owner"
    },
    {
      "lan_id": "jane456",
      "email": "jane@company.com",
      "name": "Jane Smith",
      "role": "Viewer"
    }
  ]
}

5.2 Add Users to Logical Group

    Endpoint: POST /api/groups/{logical_group_id}/users

Payload:
{
  "users": [
    {
      "lan_id": "john123",
      "role": "Editor"
    },
    {
      "lan_id": "jane456",
      "role": "Viewer"
    }
  ]
}

Response:
{ "status": "success" }

5.3 Remove Users from Logical Group

    Endpoint: DELETE /api/groups/{logical_group_id}/users
Payload:
{
  "lan_ids": ["john123", "jane456"]
}
Response:
{ "status": "success" }

5.4 Update User Role

    Endpoint: PUT /api/groups/{logical_group_id}/users/{lan_id}/role
Payload:
{ "role": "Owner" }
Response:
{ "status": "success" }

#### Benefits of This Design

- Integration with AD:
    Automatically fetch and validate user details using LAN IDs or AD email IDs.
- Role-Based Control:
    Flexible role assignment ensures secure and organized group management.
- Batch Operations:
    Support for batch user addition or removal simplifies admin workflows.
- Error Prevention:
    Clear validation and error handling prevent conflicts or invalid inputs.



### Group Ownership with Individual Attribution

#### How It Works

1. Logical Group Ownership:
    Each rule/ruleset is formally owned by a logical group.
2. Individual Attribution:
    Track and display the user who created or last modified the rule/ruleset.

#### Advantages

- Best of Both Worlds:
    Logical groups ensure collaboration and scalability.
    Individual attribution ensures accountability and traceability.
- Easy Transitions:
    If a user leaves or changes roles, rules/rulesets remain accessible to the group.
- Activity logs ensure that contributions are tracked.

#### Recommendation

    Choose Logical Group Ownership with Individual Attribution
    This hybrid approach combines the strengths of both models:

    - Rules/rulesets belong to logical groups, ensuring scalability, collaboration, and continuity.
    - Individual attribution tracks who created or last modified a rule/ruleset, ensuring accountability.



#### Implementation Details

1. Metadata for Rules/Rulesets

    Logical Group Ownership:

{
  "rule_id": "123",
  "name": "Prohibited Phrases",
  "group": "Marketing → Content Team",
  "created_by": "john123",
  "last_modified_by": "jane456",
  "last_modified_at": "2024-11-17T10:00:00Z"
}

2. Role-Based Permissions

    Logical groups manage access based on roles:
    - Owner (Logical Group): Full control of rules/rulesets.
    - Editor: Can modify rules/rulesets.
    - Viewer: Read-only access.

3. Activity Logs
    Maintain an audit trail for all actions:
{
  "rule_id": "123",
  "action": "modified",
  "user": "jane456",
  "timestamp": "2024-11-17T10:00:00Z",
  "details": "Updated validation logic."
}

4. User Interface Design


+-----------------------------------------------+
| Rule/Ruleset Ownership Display              |
+-----------------------------------------------+
| Rule Details: Prohibited Phrases              |
+-----------------------------------------------+
| Group: Marketing → Content Team               |
| Created By: John Doe (LAN ID: john123)         |
| Last Modified By: Jane Smith (LAN ID: jane456)|
| Last Modified At: 17-Nov-2024, 10:00 AM       |
|                                               |
| Permissions:                                  |
| - Group Owners: Full Control                  |
| - Group Editors: Can Edit                     |
| - Group Viewers: Read-Only Access             |
+-----------------------------------------------+

#### APIs for Ownership and Attribution
1. Create Rule/Ruleset

    Endpoint: POST /api/rules

Payload:
{
  "name": "Prohibited Phrases",
  "group": "Marketing → Content Team",
  "created_by": "john123"
}
Response:
{ "status": "success", "rule_id": "123" }

2. Transfer Ownership

    Endpoint: PUT /api/rules/{rule_id}/ownership

Payload:
{
  "new_group": "Compliance → Legal Team"
}

Response:
{ "status": "success" }

3. View Activity Logs

    Endpoint: GET /api/rules/{rule_id}/activity
Response:
{
  "logs": [
    {
      "action": "created",
      "user": "john123",
      "timestamp": "2024-11-01T10:00:00Z"
    },
    {
      "action": "modified",
      "user": "jane456",
      "timestamp": "2024-11-17T10:00:00Z",
      "details": "Updated validation logic."
    }
  ]
}
