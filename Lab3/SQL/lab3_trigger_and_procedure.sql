DELIMITER **
CREATE TRIGGER 'update_log' before update ON 'Changes_project_status'
FOR EACH ROW BEGIN
		declare p,c,t varchar(80);
    call projectHistory_proc(p, OLD.id_project, NEW.id_project);
    call customerHistory_proc(c, OLD.id_customer, NEW.id_customer);
    call teamHistory_proc(t, OLD.id_team, NEW.id_team);
    INSERT INTO History Set
    Changes_project_status_Id = OLD.Id,
    ProjectHistory = p,
    CustomerHistory = c,
    TeamHistory = t;
END;
**

**
create procedure 'projectHistory_proc' (out res varchar(80), in oldId int, in newId int) deterministic
begin
	if oldId != newId then
		set res = concat_ws(' -> ',(select t.Name from Projects t where oldId = t.Id),
			(select t.Name from Projects t where newId = t.Id));
	end if;
end;
**

**
create procedure 'customerHistory_proc' (out res varchar(80), in oldId int, in newId int) deterministic
begin
	if oldId != newId then
		set res = concat_ws(' -> ',(select t.Name from Customers t where oldId = t.Id),
			(select t.Name from Customers t where newId = t.Id));
	end if;
end;
**

**
create procedure 'teamHistory_proc' (out res varchar(80), in oldId int, in newId int) deterministic
begin
	if oldId != newId then
		set res = concat_ws(' -> ',(select t.Name from Teams t where oldId = t.Id),
			(select t.Name from Teams t where newId = t.Id));
	end if;
end;
**