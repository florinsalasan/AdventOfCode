open Str

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

        let list1 = ref [] in
        let list2 = ref [] in

        List.iter (fun line -> 
            let parts = Str.(split (regexp " ") line) in
            match parts with 
            | [part1; part2] ->
              list1 := int_of_string part1 :: !list1;
              list2 := int_of_string part2 :: !list2
            | _ -> assert false
        ) !lines;

        let list1 = List.sort compare !list1 in
        let list2 = List.sort compare !list2 in

        let rec sum lists = 
            match lists with
            | ([], []) -> 0
            | (x :: xs, y :: ys) -> abs (x - y) + sum (xs, ys)
            | _ -> assert false

        in
        let sum2 = sum (list1, list2) in
        print_endline ("Sum: " ^ string_of_int sum2)
        

