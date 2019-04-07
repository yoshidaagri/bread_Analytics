DELIMITER //

-- IF EXISTS 句は MySQL 拡張です。
-- これは、プロシージャーまたは関数が存在しない場合にエラーが発生しないようにします。SHOW WARNINGS で表示できる警告が生成されます。
DROP PROCEDURE IF EXISTS p_bread_shops_main_products //


/* ----------------------------------------------------------------- */
/* 関数名：パン屋主力商品検索                                        */
/* 引数：                                                            */
/*      OUT vRET INT          リターンコード                         */
/*      OUT vMSG VARCHAR(200) メッセージ                             */
/* 処理内容：                                                        */
/*      productsを駆動表として、1レコードずつ処理する                */
/*      products_nameをshop_homepageのheadとbodyにlike検索し、       */
/*      該当する場合shop_main_productsにIDを記録する。      　　　　 */
/* 備考：                                                            */
/*      shop_main_productsに重複がある場合は、スキップする       */
/* 標準化対応                                                        */
/*      特になし                                                     */
/* ----------------------------------------------------------------- */


CREATE PROCEDURE p_bread_shops_main_products(
--   OUT vRET INT
--  OUT vMSG VARCHAR(200)
)
EXEC_SP: BEGIN
  DECLARE vCnt            INT;
  DECLARE vShopCnt         INT;
  DECLARE vErrCnt         INT;
  DECLARE vTitleRow       INT;
  DECLARE vRow            INT;
  DECLARE vItemCnt        INT;
  DECLARE vProductsCnt    INT;
  DECLARE vShopHomePageCnt    INT;
  DECLARE vRetCode        INT;
  DECLARE vSplitCnt       INT;
  DECLARE vCodeCnt        INT;
  DECLARE vId             INT;
  DECLARE vOrderRowId     INT;
  DECLARE vTProceedsCnt   INT;
  DECLARE vTOrderManagementCnt  INT;
  DECLARE vTOrderCnt      INT;
  DECLARE vRowId          INT;
  
  DECLARE vDeleteFlg      VARCHAR(16);
  DECLARE vFlg            VARCHAR(32);  -- common_work_program_status_code(0:未処理、1:処理中、2:処理済み、9:異常)
  DECLARE vErr            VARCHAR(255);
  DECLARE vResult         VARCHAR(32);
  DECLARE vCodeType       VARCHAR(64);
  DECLARE vCodeValue      VARCHAR(32);
  DECLARE vPrefName       VARCHAR(1024);
  DECLARE vProductId      INT;
  DECLARE vProductName    VARCHAR(1024);
  DECLARE vProductName2    VARCHAR(1024);

  DECLARE vShopId         INT;
  DECLARE vDone INT;
  DECLARE vInsertMemoVal VARCHAR(1024);

  DECLARE curProductsCnt CURSOR FOR
    SELECT count(*) FROM products  
    WHERE  1=1;
    -- WHERE  product_id = 225;
  DECLARE curMain CURSOR FOR
    SELECT product_id,product_name FROM products p
    WHERE  1=1;
    -- WHERE  product_id = 225;

  DECLARE curShopHomepageCnt CURSOR FOR
    SELECT count(shop_id) FROM shop_homepage
    WHERE  head     LIKE CONCAT('%',vProductName,'%')
    or body LIKE CONCAT('%',vProductName,'%');
--    WHERE  head     LIKE CONCAT('%','クロワッサン','%')
--    or body LIKE CONCAT('%','クロワッサン','%');


  DECLARE curShopHomepage CURSOR FOR
    SELECT shop_id FROM shop_homepage
    WHERE  head     LIKE CONCAT('%',vProductName,'%')
    or body LIKE CONCAT('%',vProductName,'%');
--    WHERE  head     LIKE CONCAT('%','クロワッサン','%')
--    or body LIKE CONCAT('%','クロワッサン','%');

  -- レコードが存在しない場合、dune 変数にZEROをセットするハンドラ 
  DECLARE CONTINUE HANDLER FOR SQLSTATE '02000' SET vDone = 0; 
    
  SET time_zone='Asia/Tokyo';
--  SET vMSG    = '';

--  SET vMSG    = '0:チェック';

  OPEN  curProductsCnt;
  FETCH curProductsCnt INTO vProductsCnt;
  CLOSE curProductsCnt;

  OPEN  curMain;
  SET vCnt    = 0;
  SET vErrCnt = 0;
  WHILE vCnt < vProductsCnt DO
    
--    SET vMSG    = '2:fetch';
    FETCH curMain INTO vProductId,vProductName;

    SET vFlg = '2';
    SET vErr = '' ;
    SET vShopCnt    = 0;
    SET vShopHomePageCnt    = 0;
    -- 商品名に該当する店IDの件数取得
    OPEN  curShopHomepageCnt;
    FETCH curShopHomepageCnt INTO vShopHomePageCnt;
    CLOSE curShopHomepageCnt;
    
    OPEN  curShopHomepage;
    WHILE vShopCnt < vShopHomePageCnt DO
      FETCH curShopHomepage INTO vShopId;
      IF vFlg = '2' THEN
	      INSERT INTO shops_main_products(shop_id,product_id,memo) values(vShopId,vProductId,vProductName);
	    END IF;
      SET vShopCnt = vShopCnt + 1;
    END WHILE;
    CLOSE curShopHomepage;

    SET vCnt = vCnt + 1;
    COMMIT;
    
  END WHILE;
  
  CLOSE curMain;
  
--  SET vMSG    = concat('5:Colse');
  END;

//

DELIMITER ;
