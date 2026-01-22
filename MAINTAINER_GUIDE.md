# PNGC Registry Maintainer Guide

## Reviewing and Approving Partner Project Registrations

1. **Review the submitted registration issue:**
   - Check that all required fields are completed and the repository link is valid.
   - Confirm the project meets PNGC partner criteria.  This includes reviewing their license and documentation.

2. **Approve the registration:**
   - Add the `approved` label to the issue.
   - Ensure the issue also has the `registration` label (this is set by default via the issue template).

3. **Close the issue:**
   - Closing an issue with both `approved` and `registration` labels will automatically trigger the workflow to add the project to the registry table in `README.md`.
   - If this does not occur, check the `Actions` tab to investigate why the automation may have failed.

## Removing a Registered Project

1. **Review the removal request issue:**
   - Confirm the request is valid and the project should be removed.

2. **Approve the removal:**
   - Add the `approved` label to the issue.
   - Ensure the issue also has the `removal` label (set by the removal issue template).

3. **Close the issue:**
   - Closing an issue with both `approved` and `removal` labels will trigger the workflow to remove the project from the registry table in `README.md`.
   - If this does not occur, check the `Actions` tab to investigate why the automation may have failed.
  
## Notes

- If the workflow is skipped, check that both required labels (`approved` and `registration` or `removal`) are present before closing the issue.
- For troubleshooting workflow failures, see the Actions tab and review logs for missing dependencies or permissions.
