CREATE TABLE `banking_workspaces` (
	`tenant` text PRIMARY KEY NOT NULL,
	`version` integer NOT NULL,
	`contents` text NOT NULL,
	CONSTRAINT "banking_workspaces_version_positive" CHECK("banking_workspaces"."version" > 0)
);
