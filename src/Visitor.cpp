#include "Visitor.h"

// https://stackoverflow.com/questions/37962160/retrieve-lhs-rhs-value-of-operator
std::string Visitor::convertExpressionToString(clang::Expr *E) {
  clang::SourceManager &SM = context_.getSourceManager();
  clang::LangOptions lopt;

  clang::SourceLocation startLoc = E->getBeginLoc();
  clang::SourceLocation _endLoc = E->getEndLoc();
  clang::SourceLocation endLoc = clang::Lexer::getLocForEndOfToken(_endLoc, 0, SM, lopt);

  return std::string(SM.getCharacterData(startLoc), SM.getCharacterData(endLoc) - SM.getCharacterData(startLoc));
}

/**********************/
/* C++ Class traverse */
/**********************/
bool Visitor::TraverseCXXRecordDecl(clang::CXXRecordDecl *D) {

  std::string file_path = context_.getSourceManager().getFilename(D->getLocation()).str();

  std::stringstream ss(file_path);
  std::string token;
  std::vector<std::string> splitted_path;

  while (std::getline(ss, token, '/')) {
    splitted_path.push_back(token);
  }

  *getDumpFile() << "<filename> " << splitted_path[splitted_path.size() - 1] << " </filename>" << std::endl;

  *getDumpFile() <<"<class><className>" << D->getName().str() << "</className>"<< std::endl;

    if (D->getNumBases() == 1) {

        clang::CXXRecordDecl::base_class_iterator it = D->bases_begin();
        *getDumpFile() <<"<parentClass>" << it->getType().getAsString() << "</parentClass>"<< std::endl;

    }

  clang::RecursiveASTVisitor<Visitor>::TraverseCXXRecordDecl(D);
  *getDumpFile() << "</class>" << std::endl;
  return true;
}

/**********************/
/* If traverse        */
/**********************/

bool Visitor::TraverseIfStmt(clang::IfStmt *S) {
  unsigned int line = context_.getSourceManager().getPresumedLoc(S->getBeginLoc(), 1).getLine();
  *getDumpFile()<<"<if>" << line << std::endl;
  clang::RecursiveASTVisitor<Visitor>::TraverseIfStmt(S);
  *getDumpFile()<<"</if>" << std::endl;

  return true;
}

/*
 * While Stmt traverse
 * */

bool Visitor::TraverseWhileStmt(clang::WhileStmt *S) {

  unsigned int line = context_.getSourceManager().getPresumedLoc(S->getBeginLoc(), 1).getLine();
  *getDumpFile() << "<while>" << std::endl;
  clang::RecursiveASTVisitor<Visitor>::TraverseWhileStmt(S);
  *getDumpFile() << "</while>" << std::endl;
    return true;

}

/***********************/
/* C++ Method traverse */
/***********************/
bool Visitor::TraverseCXXMethodDecl(clang::CXXMethodDecl *D) {

    if (!D->isThisDeclarationADefinition()) {
        return true;
    }

    *getDumpFile() << "<method>" << std::endl;
    *getDumpFile() << "<methodName>" << D->getName().str() << "</methodName>" << std::endl;
    /*if (D->isPublic()) {
        *getDumpFile() << "<methodScope>public</methodScope>" << std::endl;
    }
    else {
        *getDumpFile() << "<methodScope>private</methodScope>" << std::endl;
    }*/
    *getDumpFile() << "<methodReturnType>" << D->getReturnType().getAsString() << "</methodReturnType>" << std::endl;

    clang::RecursiveASTVisitor<Visitor>::TraverseCXXMethodDecl(D);

    *getDumpFile() << "</method>" << std::endl;

    return true;
}

bool Visitor::TraverseFunctionDecl(clang::FunctionDecl *D) {

  *getDumpFile() << "<function> <functionName> " << D->getName().str() << "</functionName>" << std::endl;

  clang::RecursiveASTVisitor<Visitor>::TraverseFunctionDecl(D);

  *getDumpFile() << "</function>" << std::endl;
    return true;

}

bool Visitor::TraverseConditionalOperator(clang::ConditionalOperator *D) {

  *getDumpFile() << "<conditionalOperator>" << std::endl;

  clang::RecursiveASTVisitor<Visitor>::TraverseConditionalOperator(D);

  *getDumpFile() << "</conditionalOperator>" << std::endl;
    return true;

}

/*
 * Var declare
 * */

bool Visitor::VisitVarDecl(clang::VarDecl *D) {
  unsigned int line = context_.getSourceManager().getPresumedLoc(D->getBeginLoc(), 1).getLine();

  *getDumpFile() << "<var> " << D->getName().str() << " </var>" << std::endl;

  return true;
}

/*
 * Break statement visit
 * */

bool Visitor::VisitBreakStmt(clang::BreakStmt *D) {
  unsigned int line = context_.getSourceManager().getPresumedLoc(D->getBeginLoc(), 1).getLine();

  *getDumpFile() << "<break></break>" << std::endl;
  return true;

}

/*
 * Attributes visit
 * */

bool Visitor::VisitFieldDecl(clang::FieldDecl *D) {

    *getDumpFile() << "<attribute>" << std::endl;
    *getDumpFile() << "<attributeName>" << D->getName().str() << "</attributeName>" << std::endl;
    *getDumpFile() << "<attributeType>" << D->getType().getAsString() << "</attributeType>" << std::endl;
    /*if (D->isPublic()) {
        *getDumpFile() << "<attributeScope>public</attributeScope>" << std::endl;
    }
    else {
        *getDumpFile() << "<methodScope>private</methodScope>" << std::endl;
    }*/

    *getDumpFile() << "</attribute>" << std::endl;
    return true;

}

/*
 * Return statement traverse
 * */

bool Visitor::TraverseReturnStmt(clang::ReturnStmt *D) {
  unsigned int line = context_.getSourceManager().getPresumedLoc(D->getBeginLoc(), 1).getLine();

    *getDumpFile() << "<return>" << std::endl;
    clang::RecursiveASTVisitor<Visitor>::TraverseReturnStmt(D);
    *getDumpFile() << "</return>" << std::endl;
  return true;
}

bool Visitor::VisitContinueStmt(clang::ContinueStmt *D) {
  unsigned int line = context_.getSourceManager().getPresumedLoc(D->getBeginLoc(), 1).getLine();

    *getDumpFile() << "<continue></continue>" << std::endl;
  return true;

}


bool Visitor::TraverseForStmt(clang::ForStmt *D) {
  unsigned int line = context_.getSourceManager().getPresumedLoc(D->getBeginLoc(), 1).getLine();

    *getDumpFile() << "<for>" << std::endl;
    clang::RecursiveASTVisitor<Visitor>::TraverseForStmt(D);
    *getDumpFile() << "</for>" << std::endl;
  return true;

}

bool Visitor::VisitUnaryOperator(clang::UnaryOperator *D) {
  unsigned int line = context_.getSourceManager().getPresumedLoc(D->getBeginLoc(), 1).getLine();

    *getDumpFile() << "<unaryOperator></unaryOperator>" << std::endl;
  return true;

}

bool Visitor::VisitBinaryOperator(clang::BinaryOperator *D) {

    unsigned int line = context_.getSourceManager().getPresumedLoc(D->getBeginLoc(), 1).getLine();
    *getDumpFile() << "<binaryOperator>" << line;

    std::string op = D->getOpcodeStr().data();
    if (op == "=") {
        *getDumpFile() << ":" << op;
    }

    if (D->isAssignmentOp()) {
        clang::Expr* lhs = D->getLHS();
        if (clang::DeclRefExpr *DRE = llvm::dyn_cast<clang::DeclRefExpr>(lhs)) {
            if (clang::VarDecl *VD = llvm::dyn_cast<clang::VarDecl>(DRE->getDecl())) {
                std::string var = VD->getQualifiedNameAsString();
                *getDumpFile() << ":" << var;
            }
        }
        clang::Expr* rhs = D->getRHS();
        *getDumpFile() << ":" << convertExpressionToString(rhs);
    }

    *getDumpFile() << "</binaryOperator>" << std::endl;
    return true;

}

bool Visitor::VisitCallExpr(clang::CallExpr *D) {
    clang::FunctionDecl* f = D->getDirectCallee();
    unsigned int line = context_.getSourceManager().getPresumedLoc(D->getBeginLoc(), 1).getLine();

    *getDumpFile() << "<callExpr>" << line << ":" << f->getNameInfo().getName().getAsString() << "</callExpr>" << std::endl;
    return true;

}
