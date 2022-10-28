-- insert into users (email, username, firstname, lastname, hashed_password, is_active)
-- values ('email#1', 'q', 'q', 'q', '$2b$12$6eTrFLoj9BdqeE6ligs1YOLCjwRTKTgND', 1);
-- user need to be created manually


insert into organizations (name, disabled, owner_id)
values ('Organization #1', false, 1);

insert into organizations (name, disabled, owner_id)
values ('Organization #2', false, 1);

insert into organizations (name, disabled, owner_id)
values ('Organization #3', false, 1);

insert into organizations (name, disabled, owner_id)
values ('Organization #4', false, 2);


insert into operations (order_source, order_id, additional_info, message_type, organization_id, owner_id)
values ('Order source #1', '111', 'Additional info about the problem #1', 'order_attentions', 2, 1);

insert into operations (order_source, order_id, additional_info, message_type, organization_id, owner_id)
values ('Order source #2', '222', 'Additional info about the problem #2', 'order_attentions', 2, 1);

insert into operations (order_source, order_id, additional_info, message_type, organization_id, owner_id)
values ('Order source #3', '333', 'Additional info about the problem #3', 'order_attentions', 2, 1);


insert into terminal_groups (name, address, timezone, isAlive, organization_id, payment_type_id)
values ('Terminal Group #1', 'address #1', 'timezone #1', 1, 1, 1);

insert into terminal_groups (name, address, timezone, isAlive, organization_id, payment_type_id)
values ('Terminal Group #2', 'address #2', 'timezone #2', 0, 1, 3);

insert into terminal_groups (name, address, timezone, isAlive, organization_id, payment_type_id)
values ('Terminal Group #3', 'address #3', 'timezone #3', 1, 1, 2);

insert into terminal_groups (name, address, timezone, isAlive, organization_id, payment_type_id)
values ('Terminal Group #4', 'address #4', 'timezone #4', 1, 2, 2);

insert into terminal_groups (name, address, timezone, isAlive, organization_id, payment_type_id)
values ('Terminal Group #5', 'address #5', 'timezone #5', 0, 2, 1);

insert into terminal_groups (name, address, timezone, isAlive, organization_id, payment_type_id)
values ('Terminal Group #6', 'address #6', 'timezone #6', 1, 3, 3);


insert into correlations (organization_parent_id, correlation_owner_id)
values (1, 1);

insert into correlations (organization_parent_id, correlation_owner_id)
values (1, 1);

insert into correlations (organization_parent_id, correlation_owner_id)
values (2, 1);

insert into correlations (organization_parent_id, correlation_owner_id)
values (2, 2);


insert into cancel_causes (name, is_deleted, correlation_id)
values ('cancel cause #1', true, 1);

insert into cancel_causes (name, is_deleted, correlation_id)
values ('cancel cause #2', true, 1);

insert into cancel_causes (name, is_deleted, correlation_id)
values ('cancel cause #3', true, 2);

insert into cancel_causes (name, is_deleted, correlation_id)
values ('cancel cause #4', false, 2);

insert into cancel_causes (name, is_deleted, correlation_id)
values ('cancel cause #5', true, 4);


insert into order_types (name, orderServiceType, isDeleted, externalRevision, organization_id)
values ('order type #1', 'Common', true, 0, 1);

insert into order_types (name, orderServiceType, isDeleted, externalRevision, organization_id)
values ('order type #2', 'Common', true, 0, 1);

insert into order_types (name, orderServiceType, isDeleted, externalRevision, organization_id)
values ('order type #3', 'Common', true, 0, 2);

insert into order_types (name, orderServiceType, isDeleted, externalRevision, organization_id)
values ('order type #4', 'Common', true, 0, 1);

insert into order_types (name, orderServiceType, isDeleted, externalRevision, organization_id)
values ('order type #5', 'Common', true, 0, 3);

insert into order_types (name, orderServiceType, isDeleted, externalRevision, organization_id)
values ('order type #6', 'Common', true, 0, 3);


insert into categories (name, percent, discount_id)
values ('category #1', 0, 1);

insert into categories (name, percent, discount_id)
values ('category #2', 5, 1);

insert into categories (name, percent, discount_id)
values ('category #3', 10, 1);

insert into categories (name, percent, discount_id)
values ('category #4', 0, 2);

insert into categories (name, percent, discount_id)
values ('category #5', 5, 2);

insert into categories (name, percent, discount_id)
values ('category #6', 10, 3);

insert into categories (name, percent, discount_id)
values ('category #7', 5, 3);


insert into discounts (name, percent, isCategorisedDiscount, comment, canBeAppliedSelectively, minOrderSum, mode,
                       "sum", canApplyByCardNumber, isManual, isCard, isAutomatic, isDeleted, organization_id)
values ('discount #1', 0, true, 'discount comment #1', true, 0, 'discount mode #1',
        0, true, true, true, true, true, 1);

insert into discounts (name, percent, isCategorisedDiscount, comment, canBeAppliedSelectively, minOrderSum, mode,
                       "sum", canApplyByCardNumber, isManual, isCard, isAutomatic, isDeleted, organization_id)
values ('discount #2', 0, true, 'discount comment #2', true, 0, 'discount mode #2',
        0, true, true, true, true, true, 1);

insert into discounts (name, percent, isCategorisedDiscount, comment, canBeAppliedSelectively, minOrderSum, mode,
                       "sum", canApplyByCardNumber, isManual, isCard, isAutomatic, isDeleted, organization_id)
values ('discount #3', 0, true, 'discount comment #3', true, 0, 'discount mode #3',
        0, true, true, true, true, true, 2);


insert into applicable_marketing_campaigns (payment_type_id)
values (1);

insert into applicable_marketing_campaigns (payment_type_id)
values (3);

insert into applicable_marketing_campaigns (payment_type_id)
values (2);

insert into applicable_marketing_campaigns (payment_type_id)
values (1);


insert into payment_types (code, name, comment, combinable, external_revision, is_deleted, print_cheque, payment_processing_type, payment_type_kind, organization_id, payment_id)
values ('payment type code #1', 'payment type name #1', 'payment type comment #1', true, 0, true, true, 'EXTERNAL', 'UNKNOWN', 1, 1);

insert into payment_types (code, name, comment, combinable, external_revision, is_deleted, print_cheque, payment_processing_type, payment_type_kind, organization_id, payment_id)
values ('payment type code #2', 'payment type name #2', 'payment type comment #2', true, 0, true, true, 'INTERNAL', 'CARD', 1, 1);

insert into payment_types (code, name, comment, combinable, external_revision, is_deleted, print_cheque, payment_processing_type, payment_type_kind, organization_id, payment_id)
values ('payment type code #3', 'payment type name #3', 'payment type comment #3', true, 0, true, true, 'BOTH', 'CASH', 3, 3);

insert into payment_types (code, name, comment, combinable, external_revision, is_deleted, print_cheque, payment_processing_type, payment_type_kind, organization_id, payment_id)
values ('payment type code #4', 'payment type name #4', 'payment type comment #4', true, 0, true, true, 'INTERNAL', 'CREDIT', 2, 4);

insert into payment_types (code, name, comment, combinable, external_revision, is_deleted, print_cheque, payment_processing_type, payment_type_kind, organization_id, payment_id)
values ('payment type code #5', 'payment type name #5', 'payment type comment #5', true, 0, true, true, 'BOTH', 'IIKOCARD', 4, 2);


insert into items (price, positionId, type, amount, productSizeId, comment, order_id)
values (100, 15, 'PRODUCT', 1, 22, 'items comment #1', 1);

insert into items (price, positionId, type, amount, productSizeId, comment, order_id)
values (200, 23, 'PRODUCT', 2, 43, 'items comment #2', 1);

insert into items (price, positionId, type, amount, productSizeId, comment, order_id)
values (250, 45, 'PRODUCT', 5, 5, 'items comment #3', 1);

insert into items (price, positionId, type, amount, productSizeId, comment, order_id)
values (100, 65, 'PRODUCT', 3, 23, 'items comment #4', 2);

insert into items (price, positionId, type, amount, productSizeId, comment, order_id)
values (270, 37, 'PRODUCT', 7, 16, 'items comment #5', 2);

insert into items (price, positionId, type, amount, productSizeId, comment, order_id)
values (180, 72, 'PRODUCT', 6, 25, 'items comment #6', 1);

insert into items (price, positionId, type, amount, productSizeId, comment, order_id)
values (280, 82, 'PRODUCT', 2, 54, 'items comment #7', 2);

insert into items (price, positionId, type, amount, productSizeId, comment, order_id)
values (140, 11, 'PRODUCT', 9, 222, 'items comment #8', 3);

insert into items (price, positionId, type, amount, productSizeId, comment, order_id)
values (500, 63, 'PRODUCT', 8, 43, 'items comment #9', 3);

insert into items (price, positionId, type, amount, productSizeId, comment, order_id)
values (450, 88, 'PRODUCT', 3, 54, 'items comment #10', 1);


insert into combos (name, amount, price, sourceId, programId, order_id)
values ('combo #1', 3, 22, 23, 44, 1);

insert into combos (name, amount, price, sourceId, programId, order_id)
values ('combo #2', 2, 22, 33, 65, 1);

insert into combos (name, amount, price, sourceId, programId, order_id)
values ('combo #3', 3, 2, 24, 22, 2);

insert into combos (name, amount, price, sourceId, programId, order_id)
values ('combo #4', 3, 22, 28, 25, 2);

insert into combos (name, amount, price, sourceId, programId, order_id)
values ('combo #5', 3, 22, 31, 49, 1);


insert into customers (name, surname, comment, birthdate, email, should_receive_order_status_notifications, gender, type, o2o_order_id)
values ('customer name #1', 'customer surname #1', 'customer comment #1', '1990-12-17', 'customer email #1', true, 'MALE', 'ONETIME', 1);

insert into customers (name, surname, comment, birthdate, email, should_receive_order_status_notifications, gender, type, o2o_order_id)
values ('customer name #2', 'customer surname #2', 'customer comment #2', '1995-03-15', 'customer email #2', true, 'FEMALE', 'REGULAR', 2);

insert into customers (name, surname, comment, birthdate, email, should_receive_order_status_notifications, gender, type, o2o_order_id)
values ('customer name #3', 'customer surname #3', 'customer comment #3', '1989-05-04', 'customer email #3', true, 'NOTSPECIFIED', 'ONETIME', 3);

insert into customers (name, surname, comment, birthdate, email, should_receive_order_status_notifications, gender, type, o2o_order_id)
values ('customer name #4', 'customer surname #4', 'customer comment #4', '1997-08-15', 'customer email #4', true, 'MALE', 'ONETIME', 4);


insert into payments ("sum", is_processed_externally, is_fiscalized_externally, order_id)
values (3000, true, true, 1);

insert into payments ("sum", is_processed_externally, is_fiscalized_externally, order_id)
values (2000, true, true, 2);

insert into payments ("sum", is_processed_externally, is_fiscalized_externally, order_id)
values (4500, true, true, 1);

insert into payments ("sum", is_processed_externally, is_fiscalized_externally, order_id)
values (8000, true, true, 3);

insert into payments ("sum", is_processed_externally, is_fiscalized_externally, order_id)
values (7000, true, true, 4);

insert into payments ("sum", is_processed_externally, is_fiscalized_externally, order_id)
values (6700, true, true, 1);


insert into orders (external_number, table_id, phone, guest_count, guests, tab_name, source_key, order_type_id, organization_id)
values (11, 1, '+77007770077', 5, 5, null, 'source key #1', 'order type id #1', 1);

insert into orders (external_number, table_id, phone, guest_count, guests, tab_name, source_key, order_type_id, organization_id)
values (22, 2, '+77003045085', 7, 7, null, 'source key #2', 'order type id #2', 1);

insert into orders (external_number, table_id, phone, guest_count, guests, tab_name, source_key, order_type_id, organization_id)
values (33, 3, '+77007805391', 12, 12, null, 'source key #3', 'order type id #3', 1);

insert into orders (external_number, table_id, phone, guest_count, guests, tab_name, source_key, order_type_id, organization_id)
values (44, 5, '+77004653087', 3, 3, null, 'source key #4', 'order type id #4', 2);

insert into orders (external_number, table_id, phone, guest_count, guests, tab_name, source_key, order_type_id, organization_id)
values (55, 4, '+77001143054', 23, 23, null, 'source key #5', 'order type id #5', 2);

insert into orders (external_number, table_id, phone, guest_count, guests, tab_name, source_key, order_type_id, organization_id)
values (66, 6, '+77002266817', 11, 11, null, 'source key #6', 'order type id #6', 1);

insert into orders (external_number, table_id, phone, guest_count, guests, tab_name, source_key, order_type_id, organization_id)
values (77, 7, '+77005829015', 54, 54, null, 'source key #7', 'order type id #7', 3);

insert into orders (external_number, table_id, phone, guest_count, guests, tab_name, source_key, order_type_id, organization_id)
values (88, 12, '+77009278695', 35, 35, null, 'source key #8', 'order type id #8', 3);
