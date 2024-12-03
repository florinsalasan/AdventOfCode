let () =

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

        let rec counting_valid list_of_list_ints =
            match list_of_list_ints with
            | [] -> 0
            | [head :: remainder] -> 

