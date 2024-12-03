let () =

    let module M = Map.Make (Int) in

    if Array.length Sys.argv <> 2 then
        prerr_endline "Usage: ./program <filename>"
    else
        let filename = Sys.argv.(1) in 
        let ic = open_in filename in
        let lines = ref [] in
        try
            while true do
                lines := input_line ic :: !lines
            done
        with End_of_file ->
            close_in ic;

        let list1 = ref [] in
        let list2 = ref [] in

        let count_dict : int M.t ref = ref M.empty in

        List.iter (fun line -> 
            let parts = List.filter ((<>) "") (String.split_on_char ' ' line) in
            match parts with
            | [part1; part2] ->
              list1 := int_of_string part1 :: !list1;
              list2 := int_of_string part2 :: !list2;
              let in_dict = M.mem (int_of_string part2) !count_dict in
              (match in_dict with
              | true -> count_dict := M.update (int_of_string part2) (Option.map ((+) 1)) !count_dict
              | false -> count_dict := M.add (int_of_string part2) 1 !count_dict)
            | _ -> assert false
        ) !lines;

        let rec sum_products list_items dicted =
            match list_items with
            | [] -> 0
            | item :: items -> 
              begin
                match M.find_opt item dicted with
                | None -> sum_products items dicted
                | Some value -> (item * value) + sum_products items dicted
              end
        in

        let total = sum_products !list1 !count_dict
        in
        print_endline ("Sum: " ^ string_of_int total)
        
