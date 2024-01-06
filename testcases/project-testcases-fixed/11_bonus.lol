HAI
    WAZZUP
        I HAS A start1
        I HAS A start2
        I HAS A iterations
        I HAS A dump
    BUHBYE

    I IZ proceed YR NOOB MKAY
    
    VISIBLE "\n\n\n\n\n\n\n\n\n\n\n\n-------------------------------------------------- SOFT LINE / COMMAND BREAKS"

    VISIBLE "Hello ", VISIBLE "World!"

    I IZ proceed YR NOOB MKAY

    VISIBLE "\n\n\n\n\n\n\n\n\n\n\n\n-------------------------------------------------- SPECIAL CHARACTERS IN YARNS/STRINGS"
    
    VISIBLE "(:>, :)"

    I IZ proceed YR NOOB MKAY

    VISIBLE "\n\n\n\n\n\n\n\n\n\n\n\n-------------------------------------------------- LOOP NESTING"

    VISIBLE "How many iterations? " ! , GIMMEH iterations
    iterations IS NOW A NUMBR
    start1 R 0
    start2 R 0
    IM IN YR asc1 UPPIN YR start1 TIL BOTH SAEM start1 AN iterations
		IM IN YR asc2 UPPIN YR start2 TIL BOTH SAEM start2 AN iterations
		    VISIBLE "*"!
	    IM OUTTA YR asc2
        VISIBLE "\n"!
        start2 R 0
	IM OUTTA YR asc1

    I IZ proceed YR NOOB MKAY

    VISIBLE "\n\n\n\n\n\n\n\n\n\n\n\n-------------------------------------------------- MEBBE / ELSE IF CLAUSES"

    FAIL
    O RLY?
        YA RLY
            VISIBLE "IF"
        MEBBE WIN
            VISIBLE "MEBBE WAS ALSO PRESENTED ON TEST CAST 7"
    OIC

    I IZ proceed YR NOOB MKAY

    VISIBLE "\n\n\n\n\n\n\n\n\n\n\n\n-------------------------------------------------- SUPPRESS NEW LINE (!)"

    VISIBLE "1"!
    VISIBLE "2"!
    VISIBLE "3"!
    VISIBLE "4"!
    VISIBLE "5"!
    
    I IZ proceed YR NOOB MKAY

    VISIBLE "\n\n\n\n\n\n\n\n\n\n\n\n-------------------------------------------------- SWITCH NESTING / IF-ELSE NESTING / DIFFERENT CONTROL FLOW NESTING"

    SUM OF 1 AN 0
    WTF?
        OMG 1                                       
            VISIBLE 1                               BTW <-
            2
            WTF?
                OMG 4
                    VISIBLE 4
                OMG 2                               
                    VISIBLE 2                       BTW <-
                    VISIBLE 3                       BTW <-
                    GTFO
                    VISIBLE 4
                    VISIBLE 5
                    VISIBLE 6
                OMG 1
                    VISIBLE 2
                OMGWTF
                    VISIBLE "DEFAULT"
            OIC
        OMGWTF
            FAIL
            O RLY?
                YA RLY
                    VISIBLE "YA RLY"
                NO WAI
                    VISIBLE "NO WAI"                BTW <-
                    WIN
                    O RLY?
                        YA RLY
                            VISIBLE "YA RLY"        BTW <-
                        NO WAI
                            VISIBLE "NO WAI"        
                    OIC     
            OIC                      
    OIC

    I IZ proceed YR NOOB MKAY

    VISIBLE "\n\n\n\n\nDONE! :>\n\n\n"

KTHXBYE

HOW IZ I proceed YR dump
    VISIBLE "\nPress [Enter] to proceed."!
    GIMMEH dump
IF U SAY SO
